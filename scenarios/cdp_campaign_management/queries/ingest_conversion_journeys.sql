SELECT
    *
    ,ROUND((time-LAG(time)OVER(PARTITION BY ${user_id}, activation_step_id ORDER BY time))/3600.0,1) AS time_hour_from_activation
FROM (
    SELECT
        time
        ,'Activation' AS type
        ,${user_id}
        ,CAST(activation_step_id AS VARCHAR) AS activation_step_id
        ,cv_name
        ,utm_campaign
        ,utm_medium
        ,utm_source
        ,utm_content
        ,utm_connector
        ,0 AS cv_flg
        ,0 AS val
        ,0 AS revenue
    FROM ${input_db}.${input_table_activations}
    WHERE cv_name = '${cv_name}'
    AND TD_TIME_RANGE(time, ${time_from}, ${time_to})

    UNION ALL
    SELECT
        time
        ,'Click' AS type
        ,${user_id}
        ,CAST(activation_step_id AS VARCHAR) AS activation_step_id
        ,cv_name
        ,utm_campaign
        ,utm_medium
        ,utm_source
        ,utm_content
        ,utm_connector
        ,0 AS cv_flg
        ,0 AS val
        ,0 AS revenue
    FROM ${input_db}.${input_table_clicks}
    WHERE cv_name = '${cv_name}'
    AND TD_TIME_RANGE(time, ${time_from}, ${time_to})

    UNION ALL
    SELECT
        time
        ,'Conversion' AS type
        ,${user_id}
        ,NULL AS activation_step_id
        ,cv_name
        ,NULL AS utm_campaign
        ,NULL AS utm_medium
        ,NULL AS utm_source
        ,NULL AS utm_content
        ,NULL AS utm_connector
        ,1 AS cv_flg
        ,val
        ,revenue
    FROM ${input_db}.${input_table_conversions}
    WHERE cv_name = '${cv_name}'
    AND TD_TIME_RANGE(time, ${time_from}, ${time_to})
)
-- ORDER BY ${user_id}, time
