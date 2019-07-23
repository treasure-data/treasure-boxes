SELECT
  id,code,team,action
FROM
  action_log
WHERE
  created_at > ${last_session_local_time}
