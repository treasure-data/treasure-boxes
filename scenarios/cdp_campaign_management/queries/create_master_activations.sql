DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table}(
    time bigint
    ,journey_id varchar
    ,segment_id varchar
    ,activation_type varchar
    ,activation_id varchar
    ,activation_step_id varchar
    ,syndication_id varchar
    ,activation_name varchar
    ,schedule_type varchar
    ,schedule_option varchar
    ,timezone varchar
    ,connection_id varchar
    ,connection_type varchar
    ,connection_name varchar
    ,all_columns varchar
    ,step_id varchar
    ,stage_no bigint
    ,stage_name varchar
    ,state varchar
    ,created_at varchar
    ,updated_at varchar
    ,journey_name varchar
)

