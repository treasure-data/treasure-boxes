SELECT
  td_uid
  , ${simple_mapping[target].using_column} AS ${simple_mapping[target].map_col_name}
  , MAX(access_time) AS last_access_time
  , ARRAY_DISTINCT(ARRAY_AGG(log_tbl_name)) AS log_tbl_name
FROM
  trs_td_session
WHERE
  TD_TIME_RANGE(time, ${(is_initial)?'NULL':moment(session_date).add(-1, "d").unix()}, ${moment(session_date).unix()})
  AND REGEXP_LIKE(${simple_mapping[target].using_column}, '${simple_mapping[target].reg_exp_validate}')
  ${(simple_mapping[target].filter==null)?'':'AND '+simple_mapping[target].filter}
GROUP BY
  td_uid
  , ${simple_mapping[target].using_column}
