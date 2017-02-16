select distinct
  userid as userid_original,
  row_number() over () as userid
from ratings
;
