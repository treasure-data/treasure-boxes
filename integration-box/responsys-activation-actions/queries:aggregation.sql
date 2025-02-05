SELECT 
  ${log.campaign_col} as campaign,
  COUNT(DISTINCT riid) AS cnt
FROM
  ${activation_actions_table}
GROUP BY
  1