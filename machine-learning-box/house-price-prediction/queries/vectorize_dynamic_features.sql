select
  rowid
  -- Use selected features on py> operator:
  ,${feature_query}
  ,medv as price
from
  ${target_table}
;
