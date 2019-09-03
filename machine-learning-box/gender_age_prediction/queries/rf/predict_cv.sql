-- @TD enable_cartesian_product: true
-- @TD autoconvertjoin: true
WITH test_data as (
  SELECT
    userid, features
  FROM
    rf_input 
  WHERE
    gender_age is not null
    AND rnd > ${train_rate} -- using 30% for testing
),
t2 as (
  SELECT
    userid,
    rf_ensemble(predicted.value, predicted.posteriori, model_weight) as predicted
  FROM (
	SELECT
	  t.userid,
	  p.model_weight,
	  tree_predict(p.model_id, p.model, t.features, '-classification') as predicted
	FROM
	  rf_model_cv p
	  LEFT OUTER JOIN test_data t
  ) t1
  GROUP BY
    userid
)
-- DIGDAG_INSERT_LINE
SELECT
  l.userid,
  r.label,
  l.predicted.probability,
  l.predicted.probabilities
FROM
  t2 l
  JOIN label_mapping r ON (l.predicted.label = r.label_id)

