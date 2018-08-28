select
  rowid
  -- Use top 4 correlated features, `lstat`, `rm`, `ptratio`, `indus`:
  ,quantitative_features(
    array("indus","rm","ptratio","lstat")
    -- log1p normalization for numerical values
    ,ln(indus + 1)
    ,ln(rm + 1)
    ,ln(ptratio + 1)
    ,ln(lstat + 1)
  ) as features
  ,medv as price
from
  ${target_table}
;
