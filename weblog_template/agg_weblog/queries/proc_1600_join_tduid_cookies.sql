-- set session distributed_join = 'true'
SELECT
  t1.time -- access_timeの日付
  , t1.td_client_id
  , t1.td_global_id
  , t1.max_access_time
  , t2.td_uid
  , MIN(min_access_time) OVER (PARTITION BY t2.td_uid) AS first_access_time
FROM
  tmp_bigint_ids AS t1
  LEFT JOIN tmp_tduids AS t2 ON t1.cid = t2.cid
