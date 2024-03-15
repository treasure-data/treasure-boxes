with temp1 as (
  select 
    p.id, p.name, p.description,
    json_extract(json_parse(d.permissions), '$.Authentications') as permissions
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
    CASE 
      when JSON_FORMAT(permissions2) like '%"ids"%' then JSON_EXTRACT_SCALAR(permissions2, '$.ids')
      else NULL
    END as auth_ids,
    JSON_EXTRACT_SCALAR(permissions2, '$.operation') as operation
  from temp3
), temp5 as (
  select
    id, name, description,
    split(auth_ids, ',') as auth_ids,
    operation
  from temp4
  where auth_ids is not null
), temp6 as (
  select id, name, description, auth_ids2, operation
  from temp5
  cross join unnest(auth_ids) as t(auth_ids2)
), temp7 as (
  select t.id, t.name, t.description, t.operation, t.auth_ids2 as auth_id, d.name as auth_name
  from temp6 t
  join connections_details d on t.auth_ids2 = cast(d.id as VARCHAR)
), temp8 as (
  select id, name, description, operation, auth_id, auth_name from temp7
  union all
  select id, name, description, operation, NULL as auth_id, NULL as auth_name from temp4 where auth_ids is null
) 
select * from temp8 order by 1, 4, 5
