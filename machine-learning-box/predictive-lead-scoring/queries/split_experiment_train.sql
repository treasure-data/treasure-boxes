SELECT
  *
FROM
  samples
WHERE
  -- only use closed opportunities for evaluation
  rank_in_label <= (per_label_count * ${train_sample_rate})
  AND is_closed = 1
  AND is_primary = 1
;
