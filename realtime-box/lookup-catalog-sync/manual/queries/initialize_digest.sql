CREATE TABLE IF NOT EXISTS _wf_${table_config.name}_digests AS
SELECT
  CAST(NULL AS VARCHAR) AS ${table_config.key_column},
  CAST(NULL AS BIGINT) AS payload_xxhash64
LIMIT 0
