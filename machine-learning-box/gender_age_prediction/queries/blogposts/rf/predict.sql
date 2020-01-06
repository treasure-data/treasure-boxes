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
	l.predicted.probabilities[0]  * ${f10x_factor}, -- F10x
	l.predicted.probabilities[1]  * ${f20x_factor}, -- F20x
	l.predicted.probabilities[2]  * ${f30x_factor}, -- F30x
	l.predicted.probabilities[3]  * ${m10x_factor}, -- M10x
	l.predicted.probabilities[4]  * ${m20x_factor}, -- M20x
	l.predicted.probabilities[5]  * ${m30x_factor}  -- M30x
  ) as probabilities
FROM
  t2 l
  JOIN label_mapping r ON (l.predicted.label = r.label_id)

