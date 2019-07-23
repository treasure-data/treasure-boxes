SELECT
  time -- access_timeの日付
  , td_client_id
  , td_global_id
  , MIN(access_time) AS min_access_time
  , MAX(access_time) AS max_access_time
FROM
  tmp_log_cookies
WHERE
  TD_TIME_RANGE(time, ${td.each.start_time}, ${td.each.end_time}, 'JST')
GROUP BY
  time
  , td_client_id
  , td_global_id
