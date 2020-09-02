select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time 
  ,user_email -- Inviting user
  ,resource_name -- Invited user
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'user_invite'
