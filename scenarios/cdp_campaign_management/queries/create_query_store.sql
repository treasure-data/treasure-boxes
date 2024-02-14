DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,db_name varchar
    ,table_name varchar
    ,query varchar
)