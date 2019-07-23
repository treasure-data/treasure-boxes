WITH log AS (
  SELECT
    cid
    , mapped_cid
    , gid
  FROM
    tmp_map_cid_gid
  WHERE
    cid_gid = 'n:n'
)

SELECT
  t1.cid
  , t2.mapped_cid AS mapped_cid
FROM
  log  AS t1
  LEFT JOIN log AS t2 ON t1.gid = t2.gid
GROUP BY
  t1.cid
  , t2.mapped_cid
