WITH t1 AS (
  SELECT
    is_won,
    CAST(COUNT(1) AS DOUBLE) AS cnt
  FROM
    train_${task}
  GROUP BY
    is_won
),
t2 AS (
  SELECT
    map_agg(is_won, cnt) AS kv
  FROM
    t1
)
SELECT
  -- compute downsampling rate
  (kv[0] / (kv[0] + kv[1] * ${pos_oversampling}.0)) / (kv[0] / (kv[0] + kv[1])) AS downsampling_rate
FROM
  t2
;
