WITH loop1 AS (
  SELECT
    t1.leader
    , t2.new_leader
  FROM
    tmp_unify_num_step4 AS t1
    LEFT JOIN tmp_unify_num_step4 AS t2 ON t1.new_leader = t2.leader
  GROUP BY
    t1.leader
    , t2.new_leader
)
, loop2 AS (
  SELECT
    t1.leader
    , t2.new_leader
  FROM
    loop1 AS t1
    LEFT JOIN tmp_unify_num_step4 AS t2 ON t1.new_leader = t2.leader
  GROUP BY
    t1.leader
    , t2.new_leader
)
, loop3 AS (
  SELECT
    t1.leader
    , t2.new_leader
  FROM
    loop2 AS t1
    LEFT JOIN tmp_unify_num_step4 AS t2 ON t1.new_leader = t2.leader
  GROUP BY
    t1.leader
    , t2.new_leader
)
, loop4 AS (
  SELECT
    t1.leader
    , t2.new_leader
  FROM
    loop3 AS t1
    LEFT JOIN tmp_unify_num_step4 AS t2 ON t1.new_leader = t2.leader
  GROUP BY
    t1.leader
    , t2.new_leader
)

SELECT
  t1.leader
  , MIN(t2.new_leader) AS new_leader
FROM
  loop4 AS t1
  LEFT JOIN tmp_unify_num_step4 AS t2 ON t1.new_leader = t2.leader
GROUP BY
  t1.leader
