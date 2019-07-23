SELECT
  -- fill NULLs w/ mean values
  AVG(annualrevenue) AS train_avg_annualrevenue,
  AVG(numberofemployees) AS train_avg_numberofemployees,
  -- for min-max normalization
  MAX(annualrevenue) AS train_max_annualrevenue, MIN(annualrevenue) AS train_min_annualrevenue,
  MAX(numberofemployees) AS train_max_numberofemployees, MIN(numberofemployees) AS train_min_numberofemployees
FROM
  samples_train_${task}
;
