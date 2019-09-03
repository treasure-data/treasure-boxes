-- DIGDAG_INSERT_LINE
WITH test_data as (
  SELECT
    userid, gender_age as actual
  FROM
    rf_input 
  WHERE
    gender_age is not null
    AND rnd > ${train_rate} -- using 30% for testing
)
select
  l.actual,
  r.label as predicted,
  count(1) as cnt
from
  test_data l
  JOIN rf_predicted_cv_calibrated r ON (l.userid = r.userid)
group by
  1, 2