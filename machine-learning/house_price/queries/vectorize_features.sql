select
  rowid
  ,array_concat(
    -- Use all features:
    -- quantitative_features(
    --   array("crim","zn","indus","nox","rm","age","dis","tax","ptratio","b","lstat")
    --   ,crim,zn,indus,nox,rm,age,dis,tax,ptratio,b,lstat
    -- )
    -- ,categorical_features(
    --   array("chas","rad")
    --   ,chas,rad
    -- )

    -- Use top 4 correlated features, `lstat`, `rm`, `ptratio`, `indus`:
    quantitative_features(
      array("indus","rm","ptratio","lstat")
      ,indus,rm,ptratio,lstat
    )
  ) as features
  ,medv as price
from
  ${target_table}
;
