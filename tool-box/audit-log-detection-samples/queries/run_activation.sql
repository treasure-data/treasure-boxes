select
  td_time_format(time, 'yyyy-MM-dd HH:mm;ss', 'JST') as time
  ,resource_id as avtivation_id
  ,split(resource_path, '.')[1] as audience
  ,split(resource_path, '.')[2] as segment
  ,split(resource_path, '.')[3] as activation
  ,user_id
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'syndication_run'
