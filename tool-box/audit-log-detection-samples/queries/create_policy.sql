select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_id as policy_id
  ,resource_name as policy_name
  ,user_id
  ,user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'permission_policy_create'
