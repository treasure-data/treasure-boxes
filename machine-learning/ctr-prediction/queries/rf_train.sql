WITH train_oversampling AS (
  -- negative samples
  SELECT features, label
  FROM train
  WHERE label = 0
  UNION ALL
  -- over-sampled positive samples
  SELECT features, label
  FROM (
    SELECT amplify(${pos_oversampling}, features, label) AS (features, label)
    FROM train
    WHERE label = 1
  ) t0
)
-- DIGDAG_INSERT_LINE
SELECT
  train_randomforest_classifier(
    feature_hashing(features),
    label,
    '-trees 100 -seed 31'
  ) AS (model_id, model_weight, model, var_importance, oob_errors, oob_tests)
FROM
  train_oversampling;
