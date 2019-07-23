WITH test_exploded AS (
  SELECT
    contactid,
    extract_feature(fv) AS feature,
    extract_weight(fv) AS value
  FROM
    test_${task} t1
  LATERAL VIEW
    explode(features) t2 AS fv
),
score AS (
  SELECT
    t1.contactid,
    sigmoid(SUM(p1.weight * t1.value)) AS p
  FROM
    test_exploded t1 LEFT OUTER
  JOIN
    model_${task} p1
    ON t1.feature = p1.feature
  GROUP BY
    t1.contactid
)
-- DIGDAG_INSERT_LINE
SELECT
  -- calibrated the probability to prevent negative effect of over-sampling
  t1.p / (t1.p + (1.0 - t1.p) / ${td.last_results.downsampling_rate}) AS probability,
  t1.contactid,
  t2.contact_name,
  t2.opportunityid,
  t2.opportunity_stage,
  t2.accountid,
  t2.account_name,
  t2.country,
  t2.owner
FROM
  score t1
JOIN
  samples_test_${task} t2
  ON t1.contactid = t2.id
ORDER BY
  probability DESC
;
