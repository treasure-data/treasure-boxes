SELECT
  *
FROM
  samples
WHERE
  -- only use closed opportunities for evaluation
  rnd <= 0.8 AND is_closed = 1 AND is_primary = 1
;
