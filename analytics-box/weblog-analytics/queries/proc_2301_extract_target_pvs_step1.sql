-- set session distributed_join = 'true'
WITH log_pvs AS (
  SELECT
    *
  FROM
    tmp_log_pvs
  WHERE
    TD_TIME_RANGE(time, ${td.each.start_time}, ${moment.unix(td.each.end_time).add(3, "h").unix()}, 'JST')
)
, mst_uid AS (
  SELECT
    time
    , td_client_id
    , td_uid
    , first_access_time
  FROM
    map_tduid_tdclientid_daily
  WHERE
    TD_TIME_RANGE(time, ${td.each.start_time}, ${moment.unix(td.each.end_time).add(3, "h").unix()}, 'JST')
)

SELECT
  t2.td_uid
  , t2.first_access_time
  , t1.*
FROM
  log_pvs AS t1
  INNER JOIN mst_uid AS t2 ON t1.time = t2.time AND t1.td_client_id = t2.td_client_id
