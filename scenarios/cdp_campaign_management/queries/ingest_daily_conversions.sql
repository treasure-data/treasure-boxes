SELECT
    TD_DATE_TRUNC('day', time, '${timezone}') AS time
    ,TD_TIME_STRING(time, 'd!', '${timezone}') AS date
    ,cv_name
    ,COUNT(1) AS cnt
    ,SUM(val) AS val
    ,SUM(revenue) AS revenue
FROM ${td.database}.${td.tables.conversions}
WHERE TD_TIME_RANGE(time, ${time_from}, ${time_to})
GROUP BY 1,2,3