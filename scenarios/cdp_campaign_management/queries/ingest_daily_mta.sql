SELECT *
FROM
(
    SELECT
        COALESCE(act.time,clk.time,mta.time) AS time
        ,COALESCE(act.date,clk.date,mta.date) AS date
        ,COALESCE(act.activation_step_id,clk.activation_step_id,mta.activation_step_id) AS activation_step_id
        ,CASE
            WHEN COALESCE(act.activation_step_id,clk.activation_step_id,mta.activation_step_id) IN (SELECT activation_step_id FROM ${td.tables.master_activations}) THEN 'internal'
            WHEN mta.type='Conversion' THEN 'internal'
            ELSE 'external'
        END AS is_internal_campaign_click
        ,mta.type AS type
        ,COALESCE(act.utm_source,clk.utm_source,mta.utm_source) AS utm_source
        ,COALESCE(act.utm_medium,clk.utm_medium,mta.utm_medium) AS utm_medium
        ,COALESCE(act.utm_campaign,clk.utm_campaign,mta.utm_campaign) AS utm_campaign
        ,COALESCE(act.utm_content,clk.utm_content,mta.utm_content) AS utm_content
        ,COALESCE(act.utm_connector,clk.utm_connector,mta.utm_connector) AS utm_connector
        ,COALESCE(act.cv_name,clk.cv_name,mta.cv_name) AS cv_name
        ,COALESCE(act.cnt,0) AS cnt_activations
        ,COALESCE(clk.cnt,0) AS cnt_clicks
        ,COALESCE(mta.click_cnt,0) AS cnt_clicks_related_conversion
        ,mta.conversion_cnt AS cnt_conversions
        ,cv_revenue
        ,COALESCE(acquired_person_last_click_model,0)   AS acquired_person_last_click_model
        ,COALESCE(acquired_person_first_click_model,0)  AS acquired_person_first_click_model
        ,COALESCE(acquired_person_session_model,0)      AS acquired_person_session_model
        ,COALESCE(acquired_revenue_last_click_model,0)  AS acquired_revenue_last_click_model
        ,COALESCE(acquired_revenue_first_click_model,0) AS acquired_revenue_first_click_model
        ,COALESCE(acquired_revenue_session_model,0)     AS acquired_revenue_session_model
        ,COALESCE(size_journey,0)   AS size_journey
        ,COALESCE(cnt_cv_id,0)   AS cnt_cv_id
    FROM ${td.tables.daily_activations} act
    FULL OUTER JOIN ${td.tables.daily_clicks} clk
    ON act.time = clk.time AND act.activation_step_id = clk.activation_step_id
    FULL OUTER JOIN (
        SELECT
            TD_DATE_TRUNC('day',time, '${user_timezone}') AS time
            ,TD_TIME_STRING(time, 'd!', '${user_timezone}') AS date
            ,activation_step_id
            ,type
            ,utm_source
            ,utm_medium
            ,utm_campaign
            ,utm_content
            ,utm_connector
            ,cv_name
            ,COUNT_IF(type='Conversion') AS conversion_cnt
            ,COUNT_IF(type='Click') AS click_cnt
            ,SUM(revenue) AS cv_revenue
            ,SUM(acquired_person_last_click_model)   AS acquired_person_last_click_model
            ,SUM(acquired_person_first_click_model)  AS acquired_person_first_click_model
            ,SUM(acquired_person_session_model)      AS acquired_person_session_model
            ,SUM(acquired_revenue_last_click_model)  AS acquired_revenue_last_click_model
            ,SUM(acquired_revenue_first_click_model) AS acquired_revenue_first_click_model
            ,SUM(acquired_revenue_session_model)     AS acquired_revenue_session_model
            ,SUM(size_journey) AS size_journey
            ,COUNT(DISTINCT cv_id) AS cnt_cv_id
        FROM ${td.tables.mta_conversion_journeys}
        GROUP BY 1,2,3,4,5,6,7,8,9,10
        ORDER BY date, activation_step_id
    ) mta
    ON clk.time = mta.time AND clk.activation_step_id = mta.activation_step_id
)
WHERE TD_TIME_RANGE(time, ${time_from}, ${time_to})
-- AND type <> 'Conversion'
-- ORDER BY cv_name, time DESC, activation_step_id