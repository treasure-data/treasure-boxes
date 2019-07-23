SELECT
  TD_DATE_TRUNC('day', time, 'JST') AS time -- access_timeの日付
  , td_client_id
  , td_global_id
  , time AS access_time
FROM
  ${rawdata_tables[tbl].db_name}.${rawdata_tables[tbl].tbl_name}
WHERE
  TD_TIME_RANGE(time, ${(is_initial)?'NULL':moment(session_date).add(-21, "h").unix()}, ${moment(session_date).add(3, "h").unix()})
  AND REGEXP_LIKE(td_client_id, '^(?!0{8}-0{4}-4000-8000-0{12})[-\w]{36}$')
  AND REGEXP_LIKE(td_global_id, '^(?!0{8}-0{4}-4000-8000-0{12})[-\w]{36}$')
