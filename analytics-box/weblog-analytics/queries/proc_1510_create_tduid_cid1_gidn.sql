SELECT
  cid
  , cid AS td_uid
FROM
  tmp_map_cid_gid
WHERE
  cid_gid = '1:n(1)'
GROUP BY
  cid
