SELECT
  COALESCE(t1.td_uid, t2.td_uid) AS td_uid
  , COALESCE(t1.device_category, t2.device_category) AS device_category
  , COALESCE(t1.device_detail, t2.device_detail) AS device_detail
  , COALESCE(t1.device_browser, t2.device_browser) AS device_browser
FROM
  mst_tduid_device AS t1
  FULL JOIN tmp_mst_tduid_device_step1 AS t2 ON t1.td_uid = t2.td_uid
