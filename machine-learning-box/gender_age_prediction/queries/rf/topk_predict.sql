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
		probabilities[0]  * ${f15_factor}, -- F15
		probabilities[1]  * ${f20_factor}, -- F20
		probabilities[2]  * ${f25_factor}, -- F25
		probabilities[3]  * ${f35_factor}, -- F35
		probabilities[4]  * ${f50_factor}, -- F50
		probabilities[5]  * ${m15_factor}, -- M15
		probabilities[6]  * ${m20_factor}, -- M20
		probabilities[7]  * ${m25_factor}, -- M25
		probabilities[8]  * ${m35_factor}, -- M35
		probabilities[9]  * ${m50_factor}  -- M50
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