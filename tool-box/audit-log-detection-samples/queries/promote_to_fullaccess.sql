select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_id as db_id
  ,resource_name as db_name
  ,affected_user_id as granted_user_id
  ,user_id as granting_user_id
  ,user_email as granting_user_email
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'database_permission_modify'
  and
  new_value = 'full_access'
