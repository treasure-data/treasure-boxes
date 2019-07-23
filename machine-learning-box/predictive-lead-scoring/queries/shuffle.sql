SELECT
  C.*,
  T.role,
  T.job,
  -- stratified sampling
  count(1) over (partition by is_won) as per_label_count,
  rank() over (partition by is_won order by rand()) as rank_in_label
FROM
  data C LEFT
JOIN
  title_levenshtein T
  ON C.id = T.id
;
