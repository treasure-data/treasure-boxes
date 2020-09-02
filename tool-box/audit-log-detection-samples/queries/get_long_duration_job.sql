select
  resource_id as job_id
  ,user_id
  ,user_email
  ,max(case when new_value = 'success' then time end) - min(case when new_value = 'running' then time end) as duration
from
  access
where
  td_interval(time, '-1d', 'JST')
  and
  event_name = 'job_modify'
group by
  1,2,3
having
  max(case when new_value = 'success' then time end) - min(case when new_value = 'running' then time end) >= ${threshold}
