-- DIGDAG_INSERT_LINE
WITH tmp1 as (
  select
      userid,
      array[ 
        probabilities[1] * ${f0_factor}, -- f0
        probabilities[2] * ${f1_factor}, -- f1
        probabilities[3] * ${f2_factor}, -- f2
        probabilities[4] * ${f3_factor}, -- f3
        probabilities[5] * ${m0_factor}, -- m0
        probabilities[6] * ${m1_factor}, -- m1
        probabilities[7] * ${m2_factor}, -- m2
        probabilities[8] * ${m3_factor}  -- m3
      ] as probabilities
  from
    rf_predicted_cv
),
tmp2 as (
  select
    userid, 
    probabilities,
    reduce( -- argmax(probabilities)
      probabilities,
      CAST(ROW(-infinity(), 0, 0) AS ROW(max DOUBLE, index INTEGER, argmax INTEGER)),
      (s, x) -> CAST(ROW(if(x > s.max, x, s.max), s.index + 1, if(x > s.max, s.index, s.argmax)) AS ROW(max DOUBLE, index INTEGER, argmax INTEGER)),
      s -> s.argmax
    ) as label
  from
    tmp1
)
select
  l.userid,
  l.probabilities,
  r.label
from
  tmp2 l
  JOIN label_mapping r ON (l.label = r.label_id)
