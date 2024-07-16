SELECT * FROM (
  SELECT DISTINCT
    '${session_id}' as session_id,
    '${attempt_id}' as attempt_id,
    CASE
      WHEN h.profile_id IS NULL THEN 'add'
      WHEN a.profile_id IS NULL THEN 'delete'
      ELSE '???' -- no change or modified
    END as change
    , coalesce(h.profile_id, a.profile_id) as profile_id
    --, h.*
    --, a.*
  FROM
    previous_profiles h
    FULL OUTER JOIN ${activation_actions_table} a
    ON h.profile_id = a.profile_id
)
WHERE
  change <> '???'
;