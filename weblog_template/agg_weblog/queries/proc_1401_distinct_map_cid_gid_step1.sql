WITH log AS (
  SELECT
    cid
    , COUNT(1) OVER(PARTITION BY cid) AS gid_cnt
    , gid
    , COUNT(1) OVER(PARTITION BY gid) AS cid_cnt
    , MIN(min_access_time) AS min_access_time
    , MAX(max_access_time) AS max_access_time
  FROM
    tmp_bigint_ids
  GROUP BY
    cid
    , gid
)


SELECT
  cid
  , MIN(IF(gid_cnt = 1, cid, NULL)) OVER (PARTITION BY gid) AS mapped_cid
  , gid_cnt
  , gid
  , cid_cnt
  , min_access_time
  , max_access_time
FROM
  log
