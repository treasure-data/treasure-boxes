select 
  fullname as task_name,
  ${td.last_results.query}
from ${td.tables.tasks}
group by 1
order by max(id)