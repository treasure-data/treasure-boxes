import json


# CAST(col AS JSON) / json_format requires valid JSON input, so plain strings fail.
# We manually quote and escape instead.


def _sql_null_wrap(col, inner_expr):
    return (
        f"            '\"{col}\":' || CASE WHEN {col} IS NULL THEN 'null'\n"
        f"{inner_expr}\n"
        f"                END"
    )


def _sql_string_expr(col):
    return _sql_null_wrap(col,
        f"                WHEN TRY(CAST({col} AS DOUBLE)) IS NOT NULL"
        f" THEN CAST({col} AS VARCHAR)\n"
        f"                ELSE '\"' || replace(CAST({col} AS VARCHAR),"
        f" '\"', '\\\\\"') || '\"'")


def _sql_numeric_expr(col):
    return _sql_null_wrap(col,
        f"                ELSE COALESCE("
        f"regexp_replace(CAST(TRY(CAST({col} AS DECIMAL(30,10))) AS VARCHAR),"
        f" '\\.?0+$', ''), CAST({col} AS VARCHAR))")


def _sql_array_varchar_expr(col):
    return _sql_null_wrap(col,
        f"                ELSE '[' || array_join(transform({col},"
        f" x -> CASE WHEN x IS NULL THEN 'null'"
        f" ELSE '\"' || replace(x, '\"', '\\\\\"') || '\"' END),"
        f" ',') || ']'")


def _sql_array_numeric_expr(col):
    return _sql_null_wrap(col,
        f"                ELSE '[' || array_join(transform({col},"
        f" x -> CASE WHEN x IS NULL THEN 'null'"
        f" ELSE CAST(x AS VARCHAR) END),"
        f" ',') || ']'")


def _sql_array_float_expr(col):
    return _sql_null_wrap(col,
        f"                ELSE '[' || array_join(transform({col},"
        f" x -> CASE WHEN x IS NULL THEN 'null'"
        f" ELSE COALESCE(regexp_replace("
        f"CAST(TRY(CAST(x AS DECIMAL(30,10))) AS VARCHAR),"
        f" '\\.?0+$', ''), CAST(x AS VARCHAR)) END),"
        f" ',') || ']'")


def generate_extract_sql_from_results(database, table_name, columns, column_types, **kwargs):
    import digdag

    print(f"=== generate_extract_sql_from_results called ===")
    print(f"database: {database}")
    print(f"table_name: {table_name}")
    print(f"columns type: {type(columns)}")
    print(f"columns: {columns}")
    print(f"column_types: {column_types}")

    if isinstance(columns, str):
        columns = json.loads(columns)

    if isinstance(column_types, str):
        column_types = json.loads(column_types)

    if not columns or len(columns) == 0:
        raise ValueError(f"No columns found for table {table_name}")

    if not column_types or len(column_types) != len(columns):
        raise ValueError(
            f"column_types length ({len(column_types) if column_types else 0}) "
            f"does not match columns length ({len(columns)}) for table {table_name}"
        )

    key_column = columns[0]
    print(f"Key column: {key_column}")
    print(f"Total columns: {len(columns)}")

    excluded_columns = {key_column.lower(), 'time'}

    json_parts = []
    for col, col_type in zip(columns, column_types):
        if col.lower() not in excluded_columns:
            col_type_lower = col_type.lower()
            if col_type_lower.startswith('array(varchar'):
                expr = _sql_array_varchar_expr(col)
            elif col_type_lower.startswith(('array(bigint)', 'array(integer)')):
                expr = _sql_array_numeric_expr(col)
            elif col_type_lower.startswith(('array(double)', 'array(real)')):
                expr = _sql_array_float_expr(col)
            elif col_type_lower.startswith('array('):
                raise ValueError(
                    f"Unsupported array column type '{col_type}' for column '{col}'"
                )
            elif col_type_lower in ('double', 'real'):
                expr = _sql_numeric_expr(col)
            else:
                expr = _sql_string_expr(col)
            json_parts.append(expr)

    print(f"Excluded columns: {excluded_columns}")
    print(f"Payload will include {len(json_parts)} columns")

    json_array = ',\n'.join(json_parts)

    sql = f"""-- Create or replace updated records table
  DROP TABLE IF EXISTS _wf_{table_name}_updated;

  -- Extract records that have changed (using xxhash64 digest comparison)
  CREATE TABLE _wf_{table_name}_updated AS
  SELECT
    {key_column},
    payload
  FROM (
    SELECT
      {key_column},
      '{{' || array_join(
        ARRAY[
{json_array}
        ],
        ','
      ) || '}}' AS payload
    FROM {database}.{table_name}
    WHERE {key_column} IS NOT NULL
  ) {table_name}_all
  WHERE NOT EXISTS (
    SELECT 1
    FROM _wf_{table_name}_digests dig
    WHERE dig.{key_column} = {table_name}_all.{key_column}
      AND dig.payload_xxhash64 = from_big_endian_64(xxhash64(to_utf8({table_name}_all.payload)))
  )
  """

    print("Generated SQL (first 500 chars):")
    print(sql[:500])
    print(f"SQL length: {len(sql)} chars")

    digdag.env.store({
        'extract_sql': sql,
        'key_column': key_column
    })

    return {'extract_sql': sql, 'key_column': key_column}
