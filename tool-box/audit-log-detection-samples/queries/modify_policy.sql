with source as (
  select
    td_time_format(time, 'yyyy-MM-dd HH:mm;ss', 'JST') as time
    ,id
    ,resource_id as policy_id
    ,resource_name as policy_name
    ,new_value
    ,old_value
  from
    access
  where
    td_interval(time, '-1d', 'JST')
    and
    event_name = 'permission_policy_modify'
)

,old as (
  select
    time
    ,policy_id
    ,policy_name
    ,id
    ,k as item
    ,array_sort(array_agg(json_extract_scalar(v2, '$.operation'))) as value
  from (
    select
      time
      ,policy_id
      ,policy_name
      ,id
      ,k, v
    from
      source
      cross join
      unnest(cast(json_parse(old_value) as map<varchar, array<json>>)) as t(k, v)
  ) t
  cross join
  unnest(v) as t(v2)
  group by
    1,2,3,4,5
)

,new as (
  select
    time
    ,policy_id
    ,policy_name
    ,id
    ,k as item
    ,array_sort(array_agg(json_extract_scalar(v2, '$.operation'))) as value
  from (
    select
      time
      ,policy_id
      ,policy_name
      ,id
      ,k, v
    from
      source
      cross join
      unnest(cast(json_parse(new_value) as map<varchar, array<json>>)) as t(k, v)
  ) t
  cross join
  unnest(v) as t(v2)
  group by
    1,2,3,4,5
)


select
  COALESCE(new.time, old.time) as time
  ,COALESCE(new.id, old.id) as id
  ,COALESCE(new.policy_id, old.policy_id) as policy_id
  ,COALESCE(new.policy_name, old.policy_name) as policy_name
  ,COALESCE(new.item, old.item) as item
  ,new.value as new_value
  ,old.value as old_value
from
  new 
  full outer join
  old
  on
    new.id = old.id
    and
    new.item = old.item
where
  COALESCE(new.item, old.item) != 'Integrations'
  and (
    array_join(new.value, ',') != array_join(old.value, ',')
    or
    array_join(new.value, ',') is null
    or
    array_join(old.value, ',') is null
  )
order by
  id 
