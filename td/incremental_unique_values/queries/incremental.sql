CREATE TABLE ${td.dest_db}.${td.dest_table}_${session_date_compact} AS
SELECT ${td.target_field} FROM ${td.source_table}
WHERE TD_TIME_RANGE(time, ${last_session_unixtime}, ${session_unixtime})
GROUP BY 1
UNION
SELECT ${td.target_field} FROM ${td.dest_db}.${td.dest_table}
