SELECT
  -- carrying over the previous "last_results" for training
  ${td.last_results.train_avg_annualrevenue} AS train_avg_annualrevenue,
  ${td.last_results.train_avg_numberofemployees} AS train_avg_numberofemployees,
  ${td.last_results.train_max_annualrevenue} AS train_max_annualrevenue,
  ${td.last_results.train_min_annualrevenue} AS train_min_annualrevenue,
  ${td.last_results.train_max_numberofemployees} AS train_max_numberofemployees,
  ${td.last_results.train_min_numberofemployees} AS train_min_numberofemployees,
  -- fill NULLs w/ mean values
  AVG(annualrevenue) AS test_avg_annualrevenue,
  AVG(numberofemployees) AS test_avg_numberofemployees,
  -- min-max for testing should be computed on all of observed samples (i.e., train + test samples)
  greatest(MAX(annualrevenue), ${td.last_results.train_max_annualrevenue}) AS test_max_annualrevenue,
  least(MIN(annualrevenue), ${td.last_results.train_min_annualrevenue}) AS test_min_annualrevenue,
  greatest(MAX(numberofemployees), ${td.last_results.train_max_numberofemployees}) AS test_max_numberofemployees,
  least(MIN(numberofemployees), ${td.last_results.train_min_numberofemployees}) AS test_min_numberofemployees
FROM
  samples_test_${task}
;
