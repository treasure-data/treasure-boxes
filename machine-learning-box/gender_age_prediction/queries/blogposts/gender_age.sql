select
  userid,
  (if(gender='male','M','F') ||
        CASE
           WHEN age >= 33 THEN '33~48'
           WHEN age >= 23 THEN '23~27'
           ELSE '13-17'
        END
  ) as gender_age
from
  blogposts
;
