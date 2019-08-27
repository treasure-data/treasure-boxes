WITH tmp as (
  SELECT
    train_randomforest_classifier(
      features, label, '-trees ${rf_trees} -seed ${seed} -depth ${rf_max_depth} -stratified_sampling -min_split ${min_split} -min_samples_leaf ${min_samples_leaf}',
      array(${class_weights})
    ) as (model_id, model_weight, model, var_importance, oob_errors, oob_tests)
  FROM
    rf_input
  WHERE
    gender_age is not null
    AND rnd <= ${train_rate} -- using 70% for training
)
-- DIGDAG_INSERT_LINE
SELECT
  model_id, model_weight, model, to_json(var_importance) as var_importance, oob_errors, oob_tests
FROM
  tmp
