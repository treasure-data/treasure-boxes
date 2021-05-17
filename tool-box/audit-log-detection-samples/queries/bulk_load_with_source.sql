select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_id as source_id
  ,resource_name as source_unique_id
  ,cast(split(job, '.')[2] as integer) as job_id
  ,split(job, '.')[1] as target_database
  ,td_time_format(scheduled_time, 'yyyy-MM-dd HH:mm:ss', 'JST') as scheduled_time
  ,user_id
  ,user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'data_transfer_run'
