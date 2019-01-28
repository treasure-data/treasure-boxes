insert overwrite table ${td.source_tbl}_unified
SELECT
SHA1(canonical_id) td_id,
email,
fingerprint_id, 
td_client_id
FROM ${td.source_tbl}_enriched