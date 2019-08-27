select 
  l.userid,
  COALESCE(l.gender_age, r.label) as gender_age
from
  input l
  LEFT OUTER JOIN rf_predicted r ON (l.userid = r.userid)
