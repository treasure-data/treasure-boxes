SELECT
  td_uid
  , log_tbl_name
  , access_time
  , td_session_id
  , start_time
  , record_count
  , SUM(record_count) OVER (PARTITION BY td_session_id ORDER BY access_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS accum_record_count
FROM
  tmp_session_ids_step2
