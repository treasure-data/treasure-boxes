WITH tbl_base_activations AS
(
    SELECT
        t1.time
        ,${td.user_id}
        ,cdp_customer_id
        ,t1.syndication_id
        ,COALESCE(type,'segment') AS activation_type
        ,segment_id
        ,activation_step_id
        ,activation_name
        ,segment_name
        ,connector_type
        ,journey_id
    FROM
    (
        SELECT
            time
            ,identifier AS ${td.user_id}
            ,audience_id
            ,NULL AS cdp_customer_id
            ,CAST(activation_id AS VARCHAR) AS syndication_id
            ,CAST(segment_id AS VARCHAR) AS segment_id
            ,segment_name
            ,activation_name
            ,integration_type AS connector_type
        FROM ${cdp_audience_db}.${td.tables.activation_log}
        WHERE identifier_type = '${td.user_id}'
        AND CAST(audience_id AS VARCHAR) = '${ps_id}'
        AND TD_TIME_RANGE(time,${time_from},${time_to})
    ) t1
    JOIN
    (
        SELECT
            CAST(id AS VARCHAR) AS activation_step_id
            ,JSON_EXTRACT_SCALAR(JSON_PARSE(attributes), '$.syndicationId') AS syndication_id
            ,type
            ,journey_id
        FROM ${td.monitoring.db.cdp_monitoring}.${td.monitoring.tables.journey_activation}
    ) t2
    ON t1.syndication_id = t2.syndication_id
)

SELECT
    time
    ,${td.user_id}
    ,s1.activation_step_id
    ,syndication_id
    ,activation_type
    ,activation_name
    -- ,segment_id
    -- ,segment_name
    ,journey_id
    ,cv_name
    ,utm_source
    ,utm_medium
    ,utm_campaign
    ,utm_content
    ,utm_term
    ,COALESCE(utm_connector,connector_type) AS utm_connector
FROM tbl_base_activations s1
LEFT OUTER JOIN (
    SELECT
        activation_step_id
        ,MAX_BY(cv_name,time) AS cv_name
        ,MAX_BY(utm_campaign,time) AS utm_campaign
        ,MAX_BY(utm_medium,time) AS utm_medium
        ,MAX_BY(utm_source,time) AS utm_source
        ,MAX_BY(utm_content,time) AS utm_content
        ,MAX_BY(utm_connector,time) AS utm_connector
        ,MAX_BY(utm_term,time) AS utm_term
    FROM ${td.database}.${td.tables.clicks}
    GROUP BY 1
) s2
ON s1.activation_step_id = s2.activation_step_id
