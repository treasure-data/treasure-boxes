with users as (
  select
    cast(json_extract_scalar(user, '$.id') as integer) as id
    ,json_extract_scalar(user, '$.email') as email
  from
    unnest(cast(json_extract('${http.last_content}', '$') as array<json>)) as t(user)
)

select
  users.id
  ,users.email
from
  users
where
  users.id not in ( 
    select
      distinct user_id
    from
      access
    where
      td_interval(time, '-30d', 'JST'
  )
  )
