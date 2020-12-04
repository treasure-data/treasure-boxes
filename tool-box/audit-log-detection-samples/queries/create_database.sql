select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,user_id
  ,user_email
  ,resource_id as db_id
  ,resource_name as db_name
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'database_create'
