SELECT
  C.*,
  T.role,
  T.job,
  rand() AS rnd
FROM
  data C LEFT
JOIN
  title_levenshtein T
  ON C.id = T.id
;
