DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,date varchar
    ,activation_id varchar
    ,cv_name varchar
    ,utm_source varchar
    ,utm_medium varchar
    ,utm_campaign varchar
    ,utm_connector varchar
    ,utm_content varchar
    ,utm_term varchar
    ,cnt bigint
)