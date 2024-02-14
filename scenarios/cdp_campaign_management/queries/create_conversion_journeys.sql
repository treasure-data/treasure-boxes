DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,time_s varchar
    ,type varchar
    ,${user_id} varchar
    ,activation_step_id varchar
    ,cv_name varchar
    ,cv_flg int
    ,val double
    ,revenue double
    ,time_hour_from_activation double
)
