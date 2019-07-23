SELECT
  TD_DATE_TRUNC('day', time, 'JST') AS time -- access_timeの日付
  , td_client_id
  , td_global_id
  , td_user_agent
  , td_ip
  , time AS access_time
  , td_host
  , td_path
  , td_url
  , td_title
  , td_referrer
  , '${rawdata_tables[tbl].db_name}.${rawdata_tables[tbl].tbl_name}' AS log_tbl_name
  ${td.last_results.custom_values}
FROM
  ${rawdata_tables[tbl].db_name}.${rawdata_tables[tbl].tbl_name}
WHERE
  TD_TIME_RANGE(time, ${(is_initial)?'NULL':moment(session_date).add(-21, "h").unix()}, ${moment(session_date).add(3, "h").unix()})
  AND NOT TD_PARSE_AGENT(td_user_agent)['category'] = 'crawler'
