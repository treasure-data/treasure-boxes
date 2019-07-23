SELECT
  td_uid
  , td_session_id
  , MIN_BY(access_date, time) AS access_date
  , MIN_BY(referral, time) AS referral
  , td_host
  , td_path
  , COUNT(1) AS pv
  , MIN(time)
FROM
  tmp_journey_data_step1
GROUP BY
  td_uid
  , td_session_id
  , td_host
  , td_path
