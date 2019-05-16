SELECT
  time -- access_timeの日付
  , td_client_id
  , td_global_id
  , min_access_time
  , max_access_time
  , MIN(time) OVER(PARTITION BY td_client_id) AS cid_mintime
  , ROW_NUMBER() OVER(PARTITION BY time ORDER BY min_access_time) AS cid_num
  , MIN(time) OVER(PARTITION BY td_global_id) AS gid_mintime
  , ROW_NUMBER() OVER(PARTITION BY time ORDER BY min_access_time) AS gid_num
FROM
  tmp_bigint_ids_step1
