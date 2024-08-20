WITH users AS (
  SELECT id, name
  FROM basic_monitoring.users
  WHERE email = '${td.email_to_check}'
)
SELECT 
  'SAVED QUERY' AS resource_type,
  name AS resource_name, 
  CASE  
    WHEN CRON IS NOT NULL THEN 'The schedule will be deactivated. Re-enable it manually, as necessary.'
    ELSE 'No action required. The query will be re-assigned to Account Owner.'
  END AS action_item,
  CASE
    WHEN cron IS NOT NULL THEN 'Schedule: ' || cron
    ELSE 'No schedule is set for this query'
  END AS notes 
FROM basic_monitoring.schedules
WHERE user_name IN (SELECT name FROM users)

UNION 

SELECT
  'AUDIENCE',
  name,
  'Change owner (TD Support Request) or associated CDP workflows will fail',
  NULL
FROM cdp_monitoring.parent_segments_configuration
WHERE json_extract_scalar(json_parse(createdby),'$.td_user_id') IN (SELECT CAST(id AS VARCHAR) FROM users)

UNION

SELECT DISTINCT 
  'WORKFLOW',
  'Project: ' || JSON_EXTRACT_SCALAR(json_parse(project),'$.name') || ', Workflow: ' || name,
  'Save workflow as a different user to change the workflow owner',
  'Limitation: The Treasure Data related operators in the workflow (such as td>, td_run>) fail if the td.apikey secret is not set for projects that the deleted user created.'
FROM workflow_monitoring.workflows w
JOIN workflow_monitoring.revisions r on r.revision = w.revision
WHERE json_extract_scalar(json_parse(userinfo),'$.td.user.id') IN (SELECT CAST(id AS VARCHAR) FROM users)
  AND JSON_EXTRACT_SCALAR(json_parse(project),'$.name') NOT LIKE 'cdp_%'

UNION

SELECT DISTINCT
  'INSIGHTS DATAMODEL',
  name,
  'Contact TD Support to re-assign ownership',
  null
FROM insights_monitoring.datamodels
WHERE created_by IN (SELECT id from users)

ORDER BY 1,2,3

