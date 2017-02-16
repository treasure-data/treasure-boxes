select distinct
  itemid as itemid_original,
  row_number() over () as itemid
from ${table}
;
