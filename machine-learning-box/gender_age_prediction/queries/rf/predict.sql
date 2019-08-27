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
	l.predicted.probabilities[0]  * ${f15_factor}, -- F15
	l.predicted.probabilities[1]  * ${f20_factor}, -- F20
	l.predicted.probabilities[2]  * ${f25_factor}, -- F25~
	l.predicted.probabilities[3]  * ${f35_factor}, -- F35~
	l.predicted.probabilities[4]  * ${f50_factor}, -- F50~
	l.predicted.probabilities[5]  * ${m15_factor}, -- M15
	l.predicted.probabilities[6]  * ${m20_factor}, -- M20
	l.predicted.probabilities[7]  * ${m25_factor}, -- M25~
	l.predicted.probabilities[8]  * ${m35_factor}, -- M35~
	l.predicted.probabilities[9]  * ${m50_factor}, -- M50~
  ) as probabilities
FROM
  t2 l
  JOIN label_mapping r ON (l.predicted.label = r.label_id)

