select
  td_time_format(time, 'yyyy-MM-dd HH:mm;ss', 'JST') as time
  ,resource_id as job_id
  ,user_id
  ,user_email
  ,bytesize
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'job_result_download'
  and
  format not in ('msgpack.gz', 'msgpack')
