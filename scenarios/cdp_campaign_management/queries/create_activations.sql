DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,${user_id} varchar
    ,activation_id varchar
    ,activation_step_id varchar
    ,syndication_id varchar
    ,journey_id varchar
    ,activation_type varchar
    ,activation_name varchar
    ,cv_name varchar
    ,utm_campaign varchar
    ,utm_medium varchar
    ,utm_source varchar
    ,utm_content varchar
    ,utm_connector varchar
    ,utm_term varchar
)
