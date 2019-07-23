WITH train_oversampling AS (
  -- negative samples
  SELECT
    features,
    is_won
  FROM
    train_${task}
  WHERE
    is_won = 0
  UNION ALL
  -- over-sampled positive samples
  SELECT
    features,
    is_won
  FROM (
    SELECT
      amplify(${pos_oversampling}, features, is_won) AS (features, is_won)
    FROM
      train_${task}
    WHERE
      is_won = 1
  ) t0
)
-- DIGDAG_INSERT_LINE
SELECT
  feature,
  AVG(weight) AS weight
FROM (
  SELECT
    logress(features, is_won) AS (feature, weight)
  FROM (
    SELECT
      features,
      is_won
    FROM
      train_oversampling CLUSTER BY rand(1) -- random shuffling
  ) t1
) t2
GROUP BY
  feature
;
