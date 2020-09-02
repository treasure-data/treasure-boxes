with users as (
  select
    cast(json_extract_scalar(user, '$.id') as integer) as id
    ,json_extract_scalar(user, '$.email') as email
  from
    unnest(cast(json_extract('${users}', '$') as array<json>)) as t(user)
)

,active_users as (
  select
    distinct user_id
  from
    access
  where
    td_interval(time, '-${days}d', 'JST')
)

select
  users.id
  ,users.email
from
  users
  left outer join
  active_users a
  on
    users.id = a.user_id
where
  a.user_id is null
