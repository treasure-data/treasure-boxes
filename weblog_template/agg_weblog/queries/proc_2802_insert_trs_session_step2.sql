-- set session distributed_join = 'true'
SELECT
  t1.time -- start_timeの日付
  , t1.td_uid
  , t1.first_access_time
  , t1.device_category
  , t1.device_detail
  , t1.device_browser
  , t2.${type}_session_id
  , t1.time AS start_date
  , t1.${type}_start_time AS start_time
  , t2.country_name
  , t2.prefecture_name
  , t2.city_name
  , t2.referral_source
  , t2.utm_source
  , t2.utm_medium
  , t2.utm_campaign
  , t2.utm_content
  , t2.utm_term
  , t2.organic_search_kw
  , t1.${type}_row_num AS row_num
  , t1.pv_id
  , t1.access_time
  , t1.td_client_id
  , t1.td_global_id
  , t1.td_user_agent
  , t1.td_ip
  , t1.td_host
  , t1.td_path
  , t1.td_params
  , t1.td_url
  , t1.td_referrer
  , t1.td_title
  , t1.log_tbl_name
  ${(Object.prototype.toString.call(additional_columns.from_custom_values) === '[object Array]')?','+additional_columns.from_custom_values.join():''}
  ${td.last_results.from_url_params}
FROM
  tmp_trs_session_step1 AS t1
  LEFT JOIN tmp_mst_${type}_session_id AS t2 ON t1.${type}_session_id = t2.${type}_session_id
