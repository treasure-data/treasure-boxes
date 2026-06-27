"""
Generates type-aware extract SQL for Lookup Catalog sync.

Each column is serialized to JSON with type-specific handling:
  - array(varchar): JSON array of strings with NULL element preservation
  - array(bigint/integer): JSON array of integers
  - array(double/real): JSON array of clean decimals (avoids floating-point artifacts)
  - double/real (scalar): clean decimal (avoids floating-point artifacts)
  - Other unsupported array types: raises ValueError
  - All other types: string with quote escaping, NULL-safe

The key column (first column) and the 'time' column are excluded from the payload.
"""

import json
import digdag


def _sql_null_wrap(col, inner_expr):
    return f"CASE WHEN {col} IS NULL THEN 'null' ELSE {inner_expr} END"


def _sql_string_expr(col):
    return _sql_null_wrap(
        col,
        f"CASE WHEN TRY(CAST({col} AS DOUBLE)) IS NOT NULL THEN CAST({col} AS VARCHAR) "
        f"ELSE '\"' || replace(CAST({col} AS VARCHAR), '\"', '\\\\\"') || '\"' END"
    )


def _sql_numeric_expr(col):
    return _sql_null_wrap(col, f"CAST({col} AS VARCHAR)")


def _sql_float_expr(col):
    safe_cast = f"TRY(CAST({col} AS DECIMAL(30,10)))"
    return _sql_null_wrap(
        col,
        f"COALESCE(regexp_replace(CAST({safe_cast} AS VARCHAR), '\\.?0+$', ''), CAST({col} AS VARCHAR))"
    )


def _sql_array_varchar_expr(col):
    elem = "CASE WHEN x IS NULL THEN 'null' ELSE '\"' || replace(x, '\"', '\\\\\"') || '\"' END"
    return _sql_null_wrap(col, f"'[' || array_join(transform({col}, x -> {elem}), ',') || ']'")


def _sql_array_integer_expr(col):
    elem = "CASE WHEN x IS NULL THEN 'null' ELSE CAST(x AS VARCHAR) END"
    return _sql_null_wrap(col, f"'[' || array_join(transform({col}, x -> {elem}), ',') || ']'")


def _sql_array_float_expr(col):
    safe = "TRY(CAST(x AS DECIMAL(30,10)))"
    elem = f"CASE WHEN x IS NULL THEN 'null' ELSE COALESCE(regexp_replace(CAST({safe} AS VARCHAR), '\\.?0+$', ''), CAST(x AS VARCHAR)) END"
    return _sql_null_wrap(col, f"'[' || array_join(transform({col}, x -> {elem}), ',') || ']'")


def _sql_expr_for_type(col, data_type):
    t = data_type.lower()
    if t.startswith("array(varchar"):
        return _sql_array_varchar_expr(col)
    if t.startswith(("array(bigint", "array(integer")):
        return _sql_array_integer_expr(col)
    if t.startswith(("array(double", "array(real")):
        return _sql_array_float_expr(col)
    if t.startswith("array("):
        raise ValueError(f"Unsupported array column type '{data_type}' for column '{col}'. Flatten before ingestion.")
    if t in ("double", "real"):
        return _sql_float_expr(col)
    # Default: string with quote escaping and numeric detection
    return _sql_string_expr(col)


def generate_extract_sql(database, table_name, columns, column_types=None, **kwargs):
    if isinstance(columns, str):
        columns = json.loads(columns)
    if isinstance(column_types, str):
        column_types = json.loads(column_types)

    if not columns:
        raise ValueError(f"No columns found for table {table_name}")

    if not column_types or len(column_types) != len(columns):
        raise ValueError(
            f"column_types length ({len(column_types) if column_types else 0}) "
            f"does not match columns length ({len(columns)}) for table {table_name}. "
            f"Ensure the schema query returns both columns and column_types."
        )

    key_column = columns[0]
    excluded = {key_column.lower(), "time"}

    json_parts = []
    for i, col in enumerate(columns):
        if col.lower() in excluded:
            continue
        data_type = column_types[i]
        expr = _sql_expr_for_type(col, data_type)
        json_parts.append(f"            '\"{col}\":' || {expr}")

    payload_expr = ",\n".join(json_parts)

    sql = f"""DROP TABLE IF EXISTS _wf_{table_name}_updated;

CREATE TABLE _wf_{table_name}_updated AS
SELECT
  {key_column},
  payload
FROM (
  SELECT
    {key_column},
    '{{' || array_join(
      ARRAY[
{payload_expr}
      ],
      ','
    ) || '}}' AS payload
  FROM {database}.{table_name}
) src
WHERE NOT EXISTS (
  SELECT 1
  FROM _wf_{table_name}_digests dig
  WHERE dig._key = src.{key_column}
    AND dig.payload_xxhash64 = from_big_endian_64(xxhash64(to_utf8(src.payload)))
)
"""

    digdag.env.store({"extract_sql": sql, "key_column": key_column})
    return {"extract_sql": sql, "key_column": key_column}
