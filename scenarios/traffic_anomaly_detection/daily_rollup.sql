SELECT
    TD_DATE_TRUNC('day', time) AS day,
    td_host,
    COUNT(1) AS daily_pv
FROM ${source_table}
WHERE TD_TIME_RANGE(time, TD_TIME_ADD(TD_DATE_TRUNC('day', TD_SCHEDULED_TIME()), '-60d'))
      AND element_at(TD_PARSE_AGENT(agent), 'category') NOT IN ('crawler', 'misc', 'unknown')
GROUP BY 1,2
ORDER BY 1