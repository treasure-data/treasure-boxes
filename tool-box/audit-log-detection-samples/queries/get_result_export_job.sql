select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,target_resource_id as query_job_id
  ,resource_id as export_job_id
  ,user_id
  ,user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  target_resource_id is not null
