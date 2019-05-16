-- set session distributed_join = 'true'
SELECT
  COALESCE(t2.time, t1.time) AS time
  , COALESCE(t2.td_uid, t1.td_uid) AS td_uid
  , COALESCE(t2.first_access_time, t1.first_access_time) AS first_access_time
  , COALESCE(t2.td_client_id, t1.td_client_id) AS td_client_id
  , COALESCE(t2.last_access_time, t1.last_access_time) AS last_access_time
FROM
  map_tduid_tdclientid_daily AS t1
  FULL JOIN tmp_map_tduid_tdclientid_daily_step1 AS t2 ON t1.time = t2.time AND t1.td_client_id = t2.td_client_id
