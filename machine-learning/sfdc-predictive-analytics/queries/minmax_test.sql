SELECT
  -- fill NULLs w/ mean values
  AVG(annualrevenue) AS test_avg_annualrevenue,
  AVG(numberofemployees) AS test_avg_numberofemployees,
  -- for min-max normalization
  MAX(annualrevenue) AS test_max_annualrevenue, MIN(annualrevenue) AS test_min_annualrevenue,
  MAX(numberofemployees) AS test_max_numberofemployees, MIN(numberofemployees) AS test_min_numberofemployees
FROM
  samples_test_${task}
;
