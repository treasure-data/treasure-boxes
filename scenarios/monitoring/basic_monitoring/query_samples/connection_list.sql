select 
  d.id,
  c.name,
  CASE 
    when c.url like '{%}' then JSON_EXTRACT_SCALAR(JSON_PARSE(c.url), '$.type')
    else REGEXP_EXTRACT(c.url, '(.*):\/\/.*', 1)
  END as connection_type
from connections c
join connections_details d on c.name = d.name