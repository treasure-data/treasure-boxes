-- set session distributed_join = 'true'
SELECT
  t1.time -- start_timeの日付
  , t1.td_uid
  , t1.first_access_time
  , t1.td_session_id
  , t1.start_time AS td_start_time
  , t1.td_row_num
  , t2.ga_session_id
  , t2.ga_start_time
  , t1.td_session_id * 10000 + t1.td_row_num - t2.ga_session_id + 1 AS ga_row_num
  , t1.td_session_id * 10000 + t1.td_row_num AS pv_id
  , t1.access_time
  , t1.td_client_id
  , t1.td_global_id
  , t1.td_user_agent
  , t1.td_ip
  , t1.td_host
  , TD_URL_DECODE(REGEXP_REPLACE(t1.td_path, '(&|=|http.:).*|/{2,5}', '/')) AS td_path
  , URL_EXTRACT_QUERY(t1.td_url) AS td_params
  , t1.td_url
  , t1.td_title
  , t1.td_referrer
  , t1.log_tbl_name
  ${(Object.prototype.toString.call(additional_columns.from_custom_values) === '[object Array]')?','+additional_columns.from_custom_values.join():''}
FROM
  tmp_incr_trs_session_step2 AS t1
  LEFT JOIN tmp_incr_trs_session_step3 AS t2 ON t1.td_session_id = t2.td_session_id AND t1.td_row_num = t2.td_row_num
