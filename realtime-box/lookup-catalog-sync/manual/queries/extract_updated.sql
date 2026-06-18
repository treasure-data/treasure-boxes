DROP TABLE IF EXISTS _wf_${table_config.name}_updated;

CREATE TABLE _wf_${table_config.name}_updated AS
WITH src AS (
  SELECT
    ${table_config.key_column},
    '{' || array_join(ARRAY[${table_config.col_expr}], ',') || '}' AS payload
  FROM cdp_lookup_catalog.${table_config.name}
)
SELECT
  src.${table_config.key_column},
  src.payload
FROM src
WHERE NOT EXISTS (
  SELECT 1
  FROM _wf_${table_config.name}_digests dig
  WHERE dig.${table_config.key_column} = src.${table_config.key_column}
    AND dig.payload_xxhash64 = from_big_endian_64(xxhash64(to_utf8(src.payload)))
)
