WITH log AS (
  SELECT
    td_session_id
    , td_row_num
    , IF(REGEXP_LIKE(td_url, '(\?|&)utm_') OR td_row_num = 1, td_session_id * 10000 + td_row_num, NULL) AS ga_session_id
    , IF(REGEXP_LIKE(td_url, '(\?|&)utm_') OR td_row_num = 1, access_time, NULL) AS ga_start_time
  FROM
    tmp_incr_trs_session_step2
)

SELECT
  td_session_id
  , td_row_num
  , MAX(ga_session_id) OVER (PARTITION BY td_session_id ORDER BY td_row_num ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ga_session_id
  , MAX(ga_start_time) OVER (PARTITION BY td_session_id ORDER BY td_row_num ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ga_start_time
FROM
  log
