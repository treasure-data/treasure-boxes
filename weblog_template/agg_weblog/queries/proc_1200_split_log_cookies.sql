WITH count_by_time AS (
  SELECT
    time -- access_timeの日付
    , SUM(rec_cnt) OVER (ORDER BY time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_rec_cnt
  FROM (
    SELECT
      time
      , COUNT(1) AS rec_cnt
    FROM
      tmp_log_cookies
    GROUP BY
      time
  )
)

SELECT
  num
  , MIN(time) AS start_time
  , COALESCE(LEAD(MIN(time)) OVER (ORDER BY num), ${moment(session_date).add(3, "h").unix()}) AS end_time
FROM (
  SELECT
    time
    , MAX(sum_rec_cnt/CAST(3*POWER(10,8) AS INTEGER)) OVER (PARTITION BY time) AS num
  FROM
    count_by_time
)
GROUP BY
  num
ORDER BY
  num
