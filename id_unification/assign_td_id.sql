insert overwrite table ${td.source_tbl}_unified
SELECT
  SHA1(canonical_id) td_id,
  ${id1},
  ${id2}, 
  ${id3}
FROM 
  ${td.source_tbl}_enriched