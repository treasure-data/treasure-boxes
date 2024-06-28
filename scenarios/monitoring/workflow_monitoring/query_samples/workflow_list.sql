with latest_revision_per_project as (
  select 
    projectid, 
    revision,
    JSON_EXTRACT_SCALAR(JSON_PARSE(MAX_BY(userinfo, createdat)), '$.td.user.id') as user_id,
    JSON_EXTRACT_SCALAR(JSON_PARSE(MAX_BY(userinfo, createdat)), '$.td.user.name') as user_name,
    JSON_EXTRACT_SCALAR(JSON_PARSE(MAX_BY(userinfo, createdat)), '$.td.user.email') as user_email
  from revisions
  group by projectid, revision
)
select
  w.id as workflow_id,
  w.name as workflow_name,
  w.timezone,
  JSON_EXTRACT_SCALAR(JSON_PARSE(w.project), '$.id') as project_id,
  JSON_EXTRACT_SCALAR(JSON_PARSE(w.project), '$.name') as project_name,
  r.user_id,
  r.user_name,
  r.user_email
from workflows w
join latest_revision_per_project r on w.revision = r.revision
order by 4,1