select 
  TD_TIME_FORMAT(time, 'yyyy-MM-dd HH') as utc_date_hour,
  type,
  count(*) as num
from jobs
where TD_INTERVAL(time, '-1d/now')
group by 1, 2
order by 1, 2