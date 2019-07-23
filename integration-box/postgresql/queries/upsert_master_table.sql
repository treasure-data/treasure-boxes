INSERT INTO pg_master
SELECT id,code,team FROM original_master
WHERE ${last_session_local_time} < updated_at
ON CONFLICT ON CONSTRAINT constraint_name
DO UPDATE SET code=excluded.code, team=excluded.team;
