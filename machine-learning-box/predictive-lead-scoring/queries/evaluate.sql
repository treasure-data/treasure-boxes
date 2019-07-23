SELECT
  logloss(t1.probability, t2.is_won) AS logloss
FROM
  prediction_${task} t1
JOIN
  test_${task} t2
  ON t1.contactid = t2.contactid
;
