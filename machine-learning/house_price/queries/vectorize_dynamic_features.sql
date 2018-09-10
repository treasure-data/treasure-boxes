select
  rowid
  -- Use top 4 correlated features, `lstat`, `rm`, `ptratio`, `indus`:
  ,${feature_query}
  ,medv as price
from
  ${target_table}
;
