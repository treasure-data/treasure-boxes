DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,time_s varchar
    ,db_name varchar
    ,table_name varchar
    ,${td.user_id} varchar
    ,activation_step_id varchar
    ,cv_name varchar
    ,utm_campaign varchar
    ,utm_medium varchar
    ,utm_source varchar
    ,utm_content varchar
    ,utm_connector varchar
    ,utm_term varchar
    ,url varchar
)