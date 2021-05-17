select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_id as job_id
  ,split(target_table, '.')[1] as target_database
  ,split(target_table, '.')[2] as target_table
  ,user_id
  ,user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  job_type = 'BulkLoadJob'
