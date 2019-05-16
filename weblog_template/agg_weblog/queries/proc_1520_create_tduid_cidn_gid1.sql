SELECT
  cid
  , MIN(cid) OVER (PARTITION BY gid) AS td_uid
FROM
  tmp_map_cid_gid
WHERE
  cid_gid = 'n:1'
