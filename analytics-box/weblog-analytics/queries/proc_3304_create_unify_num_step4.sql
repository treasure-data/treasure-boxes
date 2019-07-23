SELECT
  leader
  , leader1 AS new_leader
FROM
  tmp_unify_num_step3
UNION ALL
SELECT
  leader
  , leader2 AS new_leader
FROM
  tmp_unify_num_step3
WHERE
  leader2 IS NOT NULL
