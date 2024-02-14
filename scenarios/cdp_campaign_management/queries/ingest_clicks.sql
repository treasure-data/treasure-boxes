SELECT ${distinct}
    t1.time
    ,db_name
    ,table_name
    ,${user_column}
    ,COALESCE(CAST(t3.activation_step_id AS VARCHAR), CAST(t1.activation_step_id AS VARCHAR)) AS activation_step_id
    ,COALESCE(t3.cv_name, t1.cv_name) AS cv_name
    ,COALESCE(t3.utm_campaign, t1.utm_campaign) AS utm_campaign
    ,COALESCE(t3.utm_medium, t1.utm_medium) AS utm_medium
    ,COALESCE(t3.utm_source, t1.utm_source) AS utm_source
    ,COALESCE(t3.utm_content, t1.utm_content) AS utm_content
    ,COALESCE(t3.utm_term, t1.utm_term) AS utm_term
    ,COALESCE(t3.utm_connector, t1.utm_connector) AS utm_connector
FROM
(
    SELECT
        ${time_column} AS time
        ,'${input_db}' AS db_name
        ,'${input_table}' AS table_name
        ,${user_column_inner}
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_id}')        as activation_step_id
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_campaign}')  as utm_campaign
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_medium}')    as utm_medium
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_source}')    as utm_source
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_content}')   as utm_content
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_term}')      as utm_term
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_connector}') as utm_connector
        ,url_extract_parameter(${url_column}, '${td.utm_names.utm_cv}')        as cv_name
    FROM ${input_db}.${input_table}
    WHERE url_extract_parameter(${url_column}, '${td.utm_names.utm_campaign}') IS NOT NULL
    AND url_extract_parameter(${url_column}, '${td.utm_names.utm_medium}') IS NOT NULL
    AND url_extract_parameter(${url_column}, '${td.utm_names.utm_source}') IS NOT NULL
    AND TD_TIME_RANGE(${time_column}, ${time_from}, ${time_to})
    AND ${filter}
) t1
${join_part}
LEFT OUTER JOIN (
    SELECT
        activation_step_id
        ,utm_source
        ,utm_medium
        ,utm_campaign
        ,cv_name
        ,MAX_BY(utm_connector, time) AS utm_connector
        ,MAX_BY(utm_content,time) AS utm_content
        ,MAX_BY(utm_term, time) AS utm_term
    FROM ${campaign_db}.${master_campaigns_table}
    WHERE ${td.utm_names.utm_source} IS NOT NULL AND ${td.utm_names.utm_medium} IS NOT NULL AND ${td.utm_names.utm_campaign} IS NOT NULL
    GROUP BY 1,2,3,4,5
) t3
ON (
    t1.utm_campaign = t3.utm_campaign
    AND t1.utm_medium = t3.utm_medium
    AND t1.utm_source = t3.utm_source
)