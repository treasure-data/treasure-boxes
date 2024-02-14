SELECT
    activation_step_id
    ,utm_campaign
    ,utm_medium
    ,utm_source
    ,cv_name
    ,MAX(utm_content) AS utm_content
    ,MAX(utm_connector) AS utm_connector
    ,MAX(utm_term) AS utm_term
FROM ${td.database}.${td.tables.tmp_master_campaigns}
GROUP BY 1,2,3,4,5