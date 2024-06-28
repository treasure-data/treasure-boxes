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
  p.id as project_id,
  p.name as project_name,
  p.createdat,
  p.updatedat,
  r.user_id,
  r.user_name,
  r.user_email
from projects p
join latest_revision_per_project r on p.revision = r.revision and p.metadata = '[]'
order by 1