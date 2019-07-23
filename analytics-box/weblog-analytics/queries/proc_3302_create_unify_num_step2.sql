SELECT
  leader
  , COUNT(1) OVER(PARTITION BY leader) AS follower_cnt
  , follower
  , COUNT(1) OVER(PARTITION BY follower) AS leader_cnt
FROM
  tmp_unify_num_step1
WHERE
  leader != follower
GROUP BY
  leader
  , follower
