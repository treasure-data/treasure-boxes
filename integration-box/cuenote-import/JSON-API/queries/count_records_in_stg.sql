SELECT
  CASE
    WHEN c > 0 THEN TRUE
    ELSE FALSE
  END AS status
FROM (
    SELECT
      COUNT(*) AS c
    FROM
      ${table}_stg
  )
;
