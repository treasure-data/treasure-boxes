DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,date varchar
    ,cv_name varchar
    ,cnt bigint
    ,val double
    ,revenue double
)