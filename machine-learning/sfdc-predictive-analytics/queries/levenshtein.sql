WITH new_data AS (
  SELECT
    *
  FROM data C
  WHERE C.id NOT IN (SELECT id FROM title_levenshtein)
)
-- DIGDAG_INSERT_LINE
SELECT
  -- find minimum normalized Levenshtein distance
  each_top_k(
    -1, id, levenshtein(title, map_title) / greatest(length(title), length(map_title)),
    id, title, map_title, map_role, map_job
  ) AS (rank, dist, id, title, map_title, role, job)
FROM (
  SELECT
    C.id,
    IF (C.title IS NULL, 'others', lower(C.title)) AS title,
    lower(T.title) AS map_title,
    T.role AS map_role,
    T.job AS map_job
  FROM
    new_data C LEFT OUTER
  JOIN
    title_mapping T
  CLUSTER BY C.id
) CT
;
