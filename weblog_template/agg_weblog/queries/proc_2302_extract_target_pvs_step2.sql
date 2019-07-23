WITH mst_uid AS (
  SELECT
    time
    , td_client_id
    , td_uid
    , first_access_time
  FROM
    map_tduid_tdclientid_daily
  WHERE
    TD_TIME_RANGE(time, ${td.each.start_time}, ${moment.unix(td.each.start_time).add(1, "d").unix()}, 'JST')
)

SELECT
  t1.td_uid
  , t1.first_access_time
  , t2.*
FROM
  mst_uid AS t1
  INNER JOIN log_pvs_for_carry_on AS t2 ON t1.time = t2.time AND t1.td_client_id = t2.td_client_id
