SELECT
  t1.time
  , t1.td_client_id
  , t1.td_global_id
  , t1.td_user_agent
  , t1.td_ip
  , t1.access_time
  , t1.td_host
  , t1.td_path
  , t1.td_url
  , t1.td_title
  , t1.td_referrer
  , t1.log_tbl_name
  ${(Object.prototype.toString.call(additional_columns.from_custom_values) === '[object Array]')?','+additional_columns.from_custom_values.join():''}
FROM
  tmp_target_pvs AS t1
  INNER JOIN (
    SELECT
      td_uid
      , log_tbl_name
      , access_time
      , td_session_id
      , start_time
    FROM
      tmp_session_ids
    WHERE
      start_time >= ${moment(session_date).unix()}
  ) AS t2 ON t1.td_uid = t2.td_uid AND t1.log_tbl_name = t2.log_tbl_name AND t1.access_time = t2.access_time
