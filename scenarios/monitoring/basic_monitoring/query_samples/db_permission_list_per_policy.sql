with temp1 as (
  select 
    p.id, p.name, p.description,
    json_extract(json_parse(d.permissions), '$.Databases') as permissions
  from policies p
  join policies_detail d on p.id = d.id
), temp2 as (
  select 
    id, name, description, CAST(permissions as ARRAY(JSON)) as permissions
  from temp1
  where permissions is not null
), temp3 as (
  select id, name, description, permissions2
  from temp2
  cross join unnest(permissions) as t(permissions2) 
), temp4 as (
  select 
    id, name, description,
    JSON_EXTRACT_SCALAR(permissions2, '$.operation') as operation,
    JSON_EXTRACT_SCALAR(permissions2, '$.ids') as target
  from temp3
) 
select 
  t4.id as policy_id, t4.name as policy_name, t4.description as policy_description, t4.operation database_operation, cast(d.id as BIGINT) as database_id, d.name as database_name
from temp4 t4
join databases d on t4.target = d.id
order by 1, 5, 4