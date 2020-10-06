select
  td_time_format(time, 'yyyy-MM-dd HH:mm:ss', 'JST')
  ,split(resource_name, '.')[1] as database
  ,split(resource_name, '.')[2] as "table"
  ,user_id
  ,user_email
  ,amount as num_records
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'table_insert_finished'
