SELECT * FROM (
  SELECT DISTINCT
    '${session_id}' as session_id,
    '${attempt_id}' as attempt_id,
    CASE
      WHEN h.${key_column} IS NULL THEN 'add'
      WHEN a.${key_column} IS NULL THEN 'delete'
      ELSE 'modified' -- no change or modified
    END as change
    , coalesce(h.${key_column}, a.${key_column}) as ${key_column}
  FROM
    previous_profiles h
    FULL OUTER JOIN ${activation_actions_table} a
    ON h.${key_column} = a.${key_column}
)
WHERE
  change != 'modified'