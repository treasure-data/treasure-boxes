SELECT
  TD_TIME_PARSE(TD_TIME_FORMAT(${tr[tbl].time}, 'yyyy-MM-dd HH:mm:ss', 'JST'), 'UTC') AS time
  , device_category
  , device_detail
  , device_browser
  ${(tr[tbl].dimension == null)?"":", "+tr[tbl].dimension.join(", ")}
  ${(tr[tbl].measure == null)?"":", "+tr[tbl].measure.join(", ")}
FROM
  agg_weblog.trs_td_session
WHERE
  ${(is_initial || tr[tbl].is_replace)?"TD_INTERVAL(time, '-6M/1M', 'JST')":"TD_INTERVAL(time, '-1d', 'JST')"}
  ${(tr[tbl].filter == null)?"":"AND "+tr[tbl].filter.join(", ")}
GROUP BY
  ${tr[tbl].time}
  , device_category
  , device_detail
  , device_browser
  ${(tr[tbl].dimension == null)?"":", "+tr[tbl].dimension.join(", ").replace(/ AS [^ ,]+(,|$)/g, ",").replace(/,$/, "")}
