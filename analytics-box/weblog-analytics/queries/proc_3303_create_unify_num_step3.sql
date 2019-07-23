SELECT
  t1.leader
  , MIN(t2.leader) AS leader1
  , MIN(IF(t1.leader < t2.leader, t2.leader, NULL)) AS leader2
FROM
  tmp_unify_num_step2 AS t1
  LEFT JOIN tmp_unify_num_step2 AS t2 ON t1.leader = t2.follower
WHERE
  NOT (
    t1.follower_cnt = 1
    AND t1.leader_cnt = 1
  )
GROUP BY
  t1.leader