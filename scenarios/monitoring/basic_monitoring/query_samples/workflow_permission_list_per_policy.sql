with temp1 as (
  select 
    p.id, p.name, p.description,
    json_extract(json_parse(d.permissions), '$.WorkflowProject') as permissions
  from policies p
  join policies_detail d on p.id = d.id
), temp2 as (
  select 
    p.id, p.name, p.description,
    json_extract(json_parse(d.permissions), '$.WorkflowProjectLevel') as permissions
  from policies p
  join policies_detail d on p.id = d.id
), temp3 as (
select * from temp1
union all
select * from temp2
), temp4 as (
  select 
    id, name, description, CAST(permissions as ARRAY(JSON)) as permissions
  from temp3
  where permissions is not null
), temp5 as (
  select id, name, description, permissions2
  from temp4
  cross join unnest(permissions) as t(permissions2)
)
select
  id, name, description,
  CASE
    when JSON_FORMAT(permissions2) like '%"name"%' then JSON_EXTRACT_SCALAR(permissions2, '$.name')
    else 'All Project'
  END as project_name,
  JSON_EXTRACT_SCALAR(permissions2, '$.operation') as operation
from temp5
order by 1,4,5