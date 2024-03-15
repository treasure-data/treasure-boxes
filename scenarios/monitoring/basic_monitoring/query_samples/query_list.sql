select 
  name, 
  type,
  query,
  user_name,
  CASE 
    when result like '{%}' then JSON_EXTRACT_SCALAR(JSON_PARSE(result), '$.type')
    else REGEXP_EXTRACT(result, '(.*):\/\/.*', 1)
  END as export_type
from schedules