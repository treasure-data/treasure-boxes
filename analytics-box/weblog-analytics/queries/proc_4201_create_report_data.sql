SELECT
  TD_TIME_PARSE(TD_TIME_FORMAT(${rd[tbl].time}, 'yyyy-MM-dd HH:mm:ss', 'JST'), 'UTC') AS time
  , device_category
  , device_detail
  , device_browser
  ${(rd[tbl].dimension == null)?"":", "+rd[tbl].dimension.join(", ")}
  ${(rd[tbl].measure == null)?"":", "+rd[tbl].measure.join(", ")}
FROM
  trs_td_session
WHERE
  ${(is_initial || rd[tbl].is_replace)?"TD_INTERVAL(time, '-6M/1M', 'JST')":"TD_INTERVAL(time, '-1d', 'JST')"}
  ${(rd[tbl].filter == null)?"":"AND "+rd[tbl].filter.join(", ")}
GROUP BY
  ${rd[tbl].time}
  , device_category
  , device_detail
  , device_browser
  ${(rd[tbl].dimension == null)?"":", "+rd[tbl].dimension.join(", ").replace(/ AS [^ ,]+(,|$)/g, ",").replace(/,$/, "")}
