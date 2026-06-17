-- @TD enable_cartesian_product: true
-- @TD autoconvertjoin: true
WITH t2 as (
  SELECT
    userid,
	rf_ensemble(predicted.value, predicted.posteriori, model_weight) as predicted
  FROM (
	SELECT
	  t.userid,
	  p.model_weight,
	  tree_predict(p.model_id, p.model, t.features, '-classification') as predicted
	FROM
	  rf_model p
	  LEFT OUTER JOIN rf_input t
  ) t1
  GROUP BY
    userid
)
-- DIGDAG_INSERT_LINE
SELECT
  l.userid,
  r.label,
  l.predicted.probability,
  l.predicted.probabilities as raw_probability,
  array( -- calibration
	l.predicted.probabilities[0]  * ${f1x_factor}, -- F1x
	l.predicted.probabilities[1]  * ${f2x_factor}, -- F2x
	l.predicted.probabilities[2]  * ${f3x_factor}, -- F3x
	l.predicted.probabilities[3]  * ${m1x_factor}, -- M1x
	l.predicted.probabilities[4]  * ${m2x_factor}, -- M2x
	l.predicted.probabilities[5]  * ${m3x_factor}  -- M3x
  ) as probabilities
FROM
  t2 l
  JOIN label_mapping r ON (l.predicted.label = r.label_id)

