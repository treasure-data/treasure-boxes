SELECT
  ${last_session_unixtime} AS time,
  user_id,
  MIN(first_access_time) AS first_access_time,
  MAX(last_access_time) AS last_access_time
FROM
  (
    SELECT
      td_client_id AS user_id,
      MIN(time) AS first_access_time,
      MAX(time) AS last_access_time
    FROM
      pageviews
    WHERE
      TD_TIME_RANGE(time, TD_TIME_ADD(${session_unixtime}, '-1d'), ${session_unixtime})
    GROUP BY
      td_client_id
    UNION ALL
    SELECT
      user_id,
      TD_FIRST(first_access_time, time) AS first_access_time,
      TD_LAST(last_access_time, time) AS last_access_time
    FROM
      pageviews_intermediate
    WHERE
      TD_TIME_RANGE(time, TD_TIME_ADD(${session_unixtime}, '-3d'), ${session_unixtime})
    GROUP BY
      user_id
   ) as tab
GROUP BY
  user_id
