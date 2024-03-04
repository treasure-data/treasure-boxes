SELECT
    IF(
        COALESCE(activation_id IN (
            SELECT DISTINCT
                activation_id
            FROM daily_activations
        ),false)
    ,1,0) AS exists_in_daily_activations
    ,utm_source
    ,utm_medium
    ,utm_campaign
    ,cv_name
    ,activation_id
    ,MAX_BY(utm_content,time) AS utm_content
    ,MAX_BY(utm_connector,time) AS utm_connector
    ,MAX_BY(utm_term,time) AS utm_term
    ,MIN(date) AS date_first_appeared
    ,MAX(date) AS date_last_appeared
    ,COUNT(1) AS cnt
    ,MIN(time) AS time
FROM ${td.database}.${td.tables.daily_clicks}
GROUP BY 1,2,3,4,5,6