-- DIGDAG_INSERT_LINE
select
   '${task_attempt_id}' as task_attempt_id,   
   '${session_time}' as session_time,
   '${user_id}' as user_id,
   '${user_email}' as user_email,
   '${model_name}' as model_name,   
   '${last_executed_notebook}.ipynb' as ipynb_url,
   '${last_executed_notebook}.html' as html_url
