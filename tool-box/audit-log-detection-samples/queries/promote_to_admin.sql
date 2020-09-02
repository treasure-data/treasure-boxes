select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_name as promoted_user  -- Promoted user
  ,user_email as promoting_user -- Promoting user
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'user_modify'
  and
  attribute_name = 'administrator'
  and
  old_value = '{"administrator":false}'
  and
  new_value = '{"administrator":true}'
