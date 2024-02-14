DROP TABLE IF EXISTS ${dest_db}.${dest_table};
CREATE TABLE IF NOT EXISTS ${dest_db}.${dest_table} (
    time bigint
    ,time_finished bigint
    ,journey_id varchar
    ,syndication_id varchar
    ,name varchar
    ,workflow_id varchar
    ,workflow_session_id varchar
    ,workflow_attempt_id varchar
    ,created_at varchar
    ,finished_at varchar
    ,status varchar
)