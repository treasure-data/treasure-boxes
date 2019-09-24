select
  userid,
  (gender || 
	CASE
	   WHEN age >= 50 THEN '50'
	   WHEN age >= 35 THEN '35'
	   WHEN age >= 24 THEN '25'
	   WHEN age >= 18 THEN '20'
	   ELSE cast(cast(round(age / 5) as int) * 5 as varchar)
	END
  ) as gender_age -- 50~, 35~, 25~, 20~, 15~
from
  source
where
  age >= ${min_age} and age <= ${max_age} -- 年齢の異常値を省く
;
