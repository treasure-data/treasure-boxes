select
  userid,
  (if(gender='male','M','F') ||
        CASE
           WHEN age >= 33 THEN '3x'
           WHEN age >= 23 THEN '2x'
           ELSE '1x'
        END
  ) as gender_age
from
  blogposts
;
