SELECT 
  TD_TIME_ADD(${session_unixtime}, '-1d') AS time,
  td_client_id AS user_id,
  MIN(time) AS first_access_time,
  MAX(time) AS last_access_time
FROM
  pageviews
WHERE
  TD_TIME_RANGE(time, NULL, TD_TIME_ADD(${session_unixtime}, '-1d'))
GROUP BY
  td_client_id
