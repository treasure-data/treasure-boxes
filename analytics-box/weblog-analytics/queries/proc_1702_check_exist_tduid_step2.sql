SELECT
  t1.time -- access_timeの日付
  , t1.td_client_id
  , t1.td_global_id
  , t1.max_access_time
  , COALESCE(t2.exist_tduid, t1.td_uid) AS td_uid
  , COALESCE(t2.first_access_time, t1.first_access_time) AS first_access_time
FROM
  tmp_tduid_cookies AS t1
  LEFT JOIN tmp_exist_tduid_step1 AS t2 ON t1.td_uid = t2.td_uid
