DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,cv_time bigint
    ,${user_id} varchar
    ,cv_id varchar
    ,position bigint
    ,time_hour_to_cv double
    ,time_hour_to_next double
    ,time_hour_from_activation double
    ,type varchar
    ,click_type varchar
    ,activation_id varchar
    ,utm_source varchar
    ,utm_medium varchar
    ,utm_campaign varchar
    ,utm_content varchar
    ,utm_connector varchar
    ,cv_name varchar
    ,size_journey bigint
    ,size_cv_session bigint
    ,is_within_cv_session bigint
    ,revenue double
    ,attr_last_click_model double
    ,attr_first_click_model double
    ,attr_session_model double
    ,acquired_person_last_click_model bigint
    ,acquired_revenue_last_click_model double
    ,acquired_person_first_click_model bigint
    ,acquired_revenue_first_click_model double
    ,acquired_person_session_model double
    ,acquired_revenue_session_model double
)
