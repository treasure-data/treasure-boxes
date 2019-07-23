WITH log AS (
  SELECT
    cid
    , COALESCE(mapped_cid, cid) AS mapped_cid
    , MAX(cid_cnt) OVER(PARTITION BY cid) AS maxcidcnt
    , gid
    , MAX(gid_cnt) OVER(PARTITION BY gid) AS maxgidcnt
    , min_access_time
    , max_access_time
  FROM
    tmp_map_cid_gid_step1
)
  
SELECT
  cid
  , mapped_cid
  , gid
  , CASE
    WHEN maxcidcnt = 1 AND maxgidcnt >= 1 THEN '1:n(1)'
    WHEN maxcidcnt > 1 AND maxgidcnt = 1 THEN 'n:1'
    WHEN maxcidcnt > 1 AND maxgidcnt > 1 THEN 'n:n'
  END AS cid_gid
  , min_access_time
  , max_access_time
FROM
  log
