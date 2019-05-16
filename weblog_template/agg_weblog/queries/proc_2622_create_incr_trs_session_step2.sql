SELECT
  TD_DATE_TRUNC('day', start_time, 'JST') AS time -- start_timeの日付
  , td_uid
  , first_access_time
  , td_session_id
  , start_time
  , accum_record_count AS td_row_num
  , access_time
  , td_client_id
  , td_global_id
  , td_user_agent
  , td_ip
  , td_host
  , td_path
  , td_url
  , td_title
  , td_referrer
  , log_tbl_name
  ${(Object.prototype.toString.call(additional_columns.from_custom_values) === '[object Array]')?','+additional_columns.from_custom_values.join():''}
FROM
  tmp_incr_trs_session_step1
WHERE
  record_count = 1
UNION ALL
SELECT
  TD_DATE_TRUNC('day', start_time, 'JST') AS time -- start_timeの日付
  , td_uid
  , first_access_time
  , td_session_id
  , start_time
  , accum_record_count + 1 - ROW_NUMBER() OVER (PARTITION BY td_session_id, access_time ORDER BY access_time) AS td_row_num
  , access_time
  , td_client_id
  , td_global_id
  , td_user_agent
  , td_ip
  , td_host
  , td_path
  , td_url
  , td_title
  , td_referrer
  , log_tbl_name
  ${(Object.prototype.toString.call(additional_columns.from_custom_values) === '[object Array]')?','+additional_columns.from_custom_values.join():''}

FROM
  tmp_incr_trs_session_step1
WHERE
  record_count != 1
