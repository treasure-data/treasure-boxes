select
  userid,
  (if(gender='male','M','F') ||
        CASE
           WHEN age >= 35 THEN '35'
           WHEN age >= 25 THEN '25'
           ELSE cast(cast(round(age / 5) as int) * 5 as varchar)
        END
  ) as gender_age -- 35~, 25~, 20~, 15~, 10~
from
  blogposts
;
