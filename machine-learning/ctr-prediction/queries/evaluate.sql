SELECT
  auc(predicted_ctr, label) AS auc,
  logloss(predicted_ctr, label) as logloss
FROM (
  SELECT t1.predicted_ctr, t2.label
  FROM prediction t1
  INNER JOIN test t2 ON (t1.rowid = t2.rowid)
  ORDER BY t1.predicted_ctr DESC
) t;
