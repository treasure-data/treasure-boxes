select
  resource_id as session_id
  ,td_time_format(min(time), 'yyyy-MM-dd HH:mm:ss', 'JST') as time
  ,if(max(case when event_name = 'bulk_import_finished' then 1 end) = 1, 'success', 'error') as status
  ,target_table
  ,user_id
  ,user_email
  ,max(
    case 
      when ip_address = 'internal' then null
      when event_name = 'bulk_import_create' then ip_address 
      else null 
    end) as ip_address
  ,max(amount) as records
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name in ('bulk_import_create', 'bulk_import_finished')
group by
  resource_id, user_id, user_email, target_table
