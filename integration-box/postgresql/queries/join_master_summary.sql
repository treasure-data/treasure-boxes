SELECT
  m.id,m.code,m.team,s.action
FROM
  pg_master m join pg_summary s ON m.id = s.id 
