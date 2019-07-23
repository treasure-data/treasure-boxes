SELECT
  td_uid
  , log_tbl_name
  , access_time
  , COUNT(1) AS record_count
  , TD_SESSIONIZE_WINDOW(access_time, 1800) OVER(PARTITION BY td_uid, log_tbl_name ORDER BY access_time) AS session_key
FROM
  tmp_target_pvs
GROUP BY
  td_uid
  , log_tbl_name
  , access_time
