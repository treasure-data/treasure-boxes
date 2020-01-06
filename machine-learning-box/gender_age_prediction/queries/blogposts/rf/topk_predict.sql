WITH test_data as (
  SELECT
    userid, collect_set(gender_age) as actual
  FROM
    rf_input 
  WHERE
    gender_age is not null
	AND rnd > ${train_rate} -- using 30% for testing
  GROUP BY
    userid
),
calibrated_prediction as (
  SELECT
	  userid,
	  array( -- calibration
		probabilities[0]  * ${f10x_factor}, -- F10x
		probabilities[1]  * ${f20x_factor}, -- F20x
		probabilities[2]  * ${f30x_factor}, -- F30x
		probabilities[3]  * ${m10x_factor}, -- M10x
		probabilities[4]  * ${m20x_factor}, -- M20x
		probabilities[5]  * ${m30x_factor}  -- M30x
	  ) as probabilities
  FROM
	  rf_predicted_cv
),
exploded as (
  select 
    l.userid,
    r.pos,
    r.prob
  from
    calibrated_prediction l
    LATERAL VIEW posexplode(l.probabilities) r as pos, prob
),
predicted as (
	select 
	  l.userid,
	  to_ordered_list(
		 r.label, -- value
		 l.prob, -- key
		 '-k ${topk_predict}'
	  ) as predicted,
	  to_ordered_list(
		 concat(r.label, ':', l.prob), -- value
		 l.prob, -- key
		 '-k ${topk_predict}'
	  ) as predicted_with_weight
	from  
	  exploded l
	  JOIN label_mapping r ON (l.pos = r.label_id)
	where
	  l.prob > 0
	group by
	  1
)
-- DIGDAG_INSERT_LINE
SELECT
  l.userid,
  l.actual,
  r.predicted,
  r.predicted_with_weight
FROM
  test_data l
  JOIN predicted r ON (l.userid = r.userid)