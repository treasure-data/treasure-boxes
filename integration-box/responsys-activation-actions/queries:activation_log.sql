SELECT 
  riid,
  '${td.last_results.campaign}' AS campaign_name,
  '${td.exec}' AS ma,
  '${session_local_time}' AS session_time_compact,
  'sent' as status,
  '${segment_name}' AS segment_name,
  '${segment_id}' AS audience_id
FROM
  ${log.database}.tmp_${activation_id}_${session_id}
GROUP BY
  1,2