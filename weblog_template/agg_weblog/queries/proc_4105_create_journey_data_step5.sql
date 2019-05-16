SELECT
  t1.td_uid
  , t2.total_session_count
  , t2.total_pv
  , t2.device_category
  , t2.device_detail
  , t2.device_browser
  , t1.td_session_id
  , t1.access_date
  , t1.referral
  , t1.td_host
  , t1.is_key_action
  , t1.td_path
  , t1.pv
FROM
  tmp_journey_data_step4 AS t1
  INNER JOIN tmp_journey_data_step2 AS t2 ON t1.td_uid = t2.td_uid
