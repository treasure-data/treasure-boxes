DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,date varchar
    ,activation_id varchar varchar
    ,is_internal_campaign_click varchar
    ,type varchar
    ,utm_source varchar
    ,utm_medium varchar
    ,utm_campaign varchar
    ,utm_content varchar
    ,utm_connector varchar
    ,cv_name varchar
    ,cnt_activations bigint
    ,cnt_clicks bigint
    ,cnt_clicks_related_conversion varchar
    ,cnt_conversions bigint
    ,cv_revenue double
    ,acquired_person_last_click_model double
    ,acquired_person_first_click_model double
    ,acquired_person_session_model double
    ,acquired_revenue_last_click_model double
    ,acquired_revenue_first_click_model double
    ,acquired_revenue_session_model double
    ,size_journey bigint
    ,cnt_cv_id varchar
)

