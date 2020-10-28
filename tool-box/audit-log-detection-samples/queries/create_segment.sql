select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,split(resource_path, '.')[1] as audience
  ,split(resource_path, '.')[2] as segment
  ,REGEXP_EXTRACT(requested_path_info, '\/audiences\/(.+)\/segments', 1) as ms_id
  ,resource_id as segment_id
  ,user_id
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'segment_create'
