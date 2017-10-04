SELECT
  first_access_day AS day,
  COUNT(1) AS uu
FROM
  (
    SELECT
      user_id,
      TD_TIME_FORMAT( TD_FIRST(first_access_time, first_access_time), 'yyyy‒MM‒dd', 'JST') AS first_access_day
    FROM
      pageviews_intermediate
    WHERE
      TD_TIME_RANGE(time, TD_TIME_ADD(${session_unixtime}, '-1d'), NULL)
    GROUP BY
      user_id
  ) first_access_table
WHERE
  first_access_day = TD_TIME_FORMAT(TD_TIME_ADD(${session_unixtime}, '-1d'), 'yyyy‒MM‒dd')
GROUP BY
  first_access_day
