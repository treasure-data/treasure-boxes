select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as created_time
  ,resource_id as ms_id
  ,resource_name as ms_name
  ,user_id
  ,user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'audience_create'
