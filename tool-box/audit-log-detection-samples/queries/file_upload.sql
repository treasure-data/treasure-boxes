select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,user_id
  ,user_email
  ,target_table
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'file_upload_import_create'
