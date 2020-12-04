select
  user_id
  ,max_by(user_email, length(user_email)) as email
  ,td_time_format(max(time), 'yyyy-MM-dd HH:mm:ss', 'JST') as last_access_time
from
  access
where
  td_interval(time, '-${days}d', 'JST')
group by
  1
