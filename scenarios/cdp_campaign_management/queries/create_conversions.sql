DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,time_s varchar
    ,${user_id} varchar
    ,val double
    ,revenue double
    ,cv_name varchar
)