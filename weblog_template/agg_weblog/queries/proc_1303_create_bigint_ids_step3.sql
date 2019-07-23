WITH log AS (
  SELECT
    time -- access_timeの日付
    , td_client_id
    , td_global_id
    , min_access_time
    , max_access_time
    , CAST(cid_mintime * POWER(10,5) AS BIGINT) AS cid_mintime
    , MIN(IF(time = cid_mintime, cid_num, NULL)) OVER(PARTITION BY td_client_id) AS cid_num
    , CAST(gid_mintime * POWER(10,5) AS BIGINT) AS gid_mintime
    , MIN(IF(time = gid_mintime, gid_num, NULL)) OVER(PARTITION BY td_global_id) AS gid_num
  FROM
    tmp_bigint_ids_step2
)

SELECT
  time -- access_timeの日付
  , td_client_id
  , td_global_id
  , min_access_time
  , max_access_time
  , cid_mintime + cid_num AS cid
  , gid_mintime + gid_num AS gid
FROM
  log
