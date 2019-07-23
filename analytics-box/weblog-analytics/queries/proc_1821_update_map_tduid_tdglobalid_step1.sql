SELECT
  TD_DATE_TRUNC('day', MIN(first_access_time), 'JST') AS time -- first_access_timeの日付
  , MIN(td_uid) AS td_uid
  , MIN(first_access_time) AS first_access_time
  , td_global_id
  , MAX(max_access_time) AS last_access_time
FROM
  tmp_exist_tduid
GROUP BY
  td_global_id
