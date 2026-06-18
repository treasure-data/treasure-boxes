DROP TABLE IF EXISTS _wf_${table_config.name}_digests_new;

CREATE TABLE _wf_${table_config.name}_digests_new AS
SELECT
  ${table_config.key_column},
  COALESCE(
    from_big_endian_64(xxhash64(to_utf8(upd.payload))),
    dig.payload_xxhash64
  ) AS payload_xxhash64
FROM _wf_${table_config.name}_updated upd
FULL OUTER JOIN _wf_${table_config.name}_digests dig
  USING (${table_config.key_column})
