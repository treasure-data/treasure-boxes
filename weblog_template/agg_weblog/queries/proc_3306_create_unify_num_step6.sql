SELECT
  COALESCE(t2.new_leader, t1.leader) AS unify_num
  , t1.follower AS td_uid
FROM
  tmp_unify_num_step1 AS t1
  LEFT JOIN tmp_unify_num_step5 AS t2 ON t1.leader = t2.leader
GROUP BY
  1,2
