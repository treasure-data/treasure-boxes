select 
  JSON_EXTRACT_SCALAR(JSON_PARSE(project), '$.id') as project_id,
  JSON_EXTRACT_SCALAR(JSON_PARSE(project), '$.name') as project_name,
  JSON_EXTRACT_SCALAR(JSON_PARSE(workflow), '$.id') as workflow_id,
  JSON_EXTRACT_SCALAR(JSON_PARSE(workflow), '$.name') as workflow_name,
  nextruntime,
  nextscheduletime
from schedules
where disabledat is null
order by 5