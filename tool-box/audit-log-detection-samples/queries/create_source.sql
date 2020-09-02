select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,resource_id as source_id
  ,resource_name as source_unique_id
  ,user_id -- User who creates the authentication
  ,user_email -- User who creates the authentication
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'data_transfer_create'
