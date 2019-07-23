WITH log AS (
  SELECT
    session_key
    , MIN(access_time) AS start_time
    , TD_DATE_TRUNC('day', MIN(access_time), 'JST') AS start_date
  FROM
    tmp_session_keys
  GROUP BY
    session_key
)

SELECT
  session_key
  , start_time
  , ROW_NUMBER() OVER (PARTITION BY start_date ORDER BY start_time) AS sid_num
FROM
  log
