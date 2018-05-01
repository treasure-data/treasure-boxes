SELECT
  train_randomforest_classifier(
    feature_hashing(features),
    label,
    '-trees ${trees} -seed 31 -stratified_sampling'
  ) AS (model_id, model_weight, model, var_importance, oob_errors, oob_tests)
FROM
  train;
