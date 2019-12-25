select
  userid,
  (if(gender='male','M','F') || cast(cast(round(age / 5) as int) * 5 as varchar)
  ) as gender_age
from
  source
;
