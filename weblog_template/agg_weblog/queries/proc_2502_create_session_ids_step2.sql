-- set session distributed_join = 'true'
SELECT
  t1.td_uid
  , t1.log_tbl_name
  , t1.access_time
  , TD_DATE_TRUNC('day', t2.start_time, 'JST') * 10000 + t2.sid_num AS td_session_id
  , t2.start_time
  , t1.record_count
FROM
  tmp_session_keys AS t1
  LEFT JOIN tmp_session_ids_step1 AS t2 ON t1.session_key = t2.session_key
