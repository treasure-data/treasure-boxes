-- set session distributed_join = 'true'
SELECT
  t1.*
  , t2.device_category
  , t2.device_detail
  , t2.device_browser
FROM
  tmp_incr_trs_session AS t1
  LEFT JOIN mst_tduid_device AS t2 ON t1.td_uid = t2.td_uid
