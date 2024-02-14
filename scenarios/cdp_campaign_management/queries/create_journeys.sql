DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table}(
    time bigint
    ,audience_id varchar
    ,id varchar
    ,name varchar
    ,state varchar
    ,created_at varchar
    ,updated_at varchar
    ,launched_at varchar
    ,allow_reentry varchar
    ,paused varchar
    ,num_stages bigint
)