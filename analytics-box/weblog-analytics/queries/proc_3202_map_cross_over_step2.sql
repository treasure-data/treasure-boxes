-- set session distributed_join = 'true'
SELECT
  COALESCE(t1.td_uid, t2.td_uid) AS td_uid
  , COALESCE(t1.${map_cross_over[target].map_col_name}, t2.${map_cross_over[target].map_col_name}) AS ${map_cross_over[target].map_col_name}
  , COALESCE(t2.last_access_time, t1.last_access_time) AS last_access_time
  , ARRAY_DISTINCT(ARRAY_UNION(COALESCE(t1.log_tbl_name, ARRAY[]), COALESCE(t2.log_tbl_name, ARRAY[]))) AS log_tbl_name
FROM
  ${map_cross_over[target].map_table} AS t1
  FULL JOIN tmp_${map_cross_over[target].map_table}_step1 AS t2 ON t1.td_uid = t2.td_uid AND t1.${map_cross_over[target].map_col_name} = t2.${map_cross_over[target].map_col_name}
