-- set session distributed_join = 'true'
SELECT
  t1.*
  , t2.td_session_id
  , t2.start_time
  , t2.record_count
  , t2.accum_record_count
FROM
  tmp_target_pvs AS t1
  INNER JOIN (
    SELECT
      td_uid
      , log_tbl_name
      , access_time
      , td_session_id
      , start_time
      , record_count
      , accum_record_count
    FROM
      tmp_session_ids
    WHERE
      start_time < ${moment(session_date).unix()}
  ) AS t2 ON t1.td_uid = t2.td_uid AND t1.log_tbl_name = t2.log_tbl_name AND t1.access_time = t2.access_time
