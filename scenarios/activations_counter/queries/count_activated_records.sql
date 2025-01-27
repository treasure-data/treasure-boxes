SELECT
  COUNT(1) AS rec_cnt,
  ${activation_id} AS act_id 
FROM
  ${activation_actions_db}.${activation_actions_table}  