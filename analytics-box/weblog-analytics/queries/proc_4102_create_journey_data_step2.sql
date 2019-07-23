SELECT
  td_uid
  , COUNT(DISTINCT td_session_id) AS total_session_count
  , COUNT(1) AS total_pv
  , MIN_BY(device_category, time) AS device_category
  , MIN_BY(device_detail, time) AS device_detail
  , MIN_BY(device_browser, time) AS device_browser
FROM
  tmp_journey_data_step1
WHERE
  TD_INTERVAL(time, '${jd.latest_access}')
GROUP BY
  td_uid
HAVING
  COUNT(1) >= ${jd.minimum_pv}
