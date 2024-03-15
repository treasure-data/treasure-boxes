with temp1 as (
  select
    p.id, p.name, p.description,
    JSON_EXTRACT(JSON_PARSE(d.permissions), '$.MasterSegmentConfig') as permissions
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
    JSON_EXTRACT_SCALAR(permissions2, '$.id') as parent_segments_id,
    JSON_EXTRACT_SCALAR(permissions2, '$.operation') as parent_segment_operation
  from temp3
), temp5 as (
  select
    t.id as policy_id, t.name as policy_name, t.description,
    t.parent_segment_operation,
    CAST(p.id as BIGINT) as parent_segment_id,
    JSON_EXTRACT_SCALAR(p.attributes, '$.name') as parent_segment_name
  from temp4 t
  join cdp_monitoring.parent_segments p on t.parent_segments_id = p.id
), temp6 as (
  select
    p.id, p.name, p.description,
    JSON_EXTRACT_SCALAR(JSON_PARSE(d.permissions), '$.Segmentation[0].operation') as parent_segment_operation
  from policies p
  join policies_detail d on p.id = d.id
), temp7 as (
  select
    id as policy_id, name as policy_name, description,
    parent_segment_operation
  from temp6
  where parent_segment_operation is not null
), temp8 as (
  select 
    policy_id, policy_name, description, parent_segment_operation, parent_segment_id, parent_segment_name
  from temp5
  union all
  select
    policy_id, policy_name, description, parent_segment_operation, NULL as parent_segment_id, NULL as parent_segment_name
  from temp7
)
select * from temp8 
order by 1, 5, 4