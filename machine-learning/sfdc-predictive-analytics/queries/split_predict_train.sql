SELECT
  *
FROM
  samples
WHERE -- train with all closed opportunities
  is_closed = 1 AND is_primary = 1
;
