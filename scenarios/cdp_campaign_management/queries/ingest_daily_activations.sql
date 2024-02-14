SELECT
    TD_DATE_TRUNC('day', time, '${timezone}') AS time
    ,TD_TIME_STRING(time, 'd!', '${timezone}') AS date
    ,activation_step_id
    ,cv_name
    ,utm_source
    ,utm_medium
    ,utm_campaign
    ,MAX_BY(utm_content,time) AS utm_content
    ,MAX_BY(utm_connector,time) AS utm_connector
    ,MAX_BY(utm_term,time) AS utm_term
    ,COUNT(1) AS cnt
FROM ${td.database}.${td.tables.activations}
WHERE TD_TIME_RANGE(time, ${time_from}, ${time_to})
GROUP BY 1,2,3,4,5,6,7
