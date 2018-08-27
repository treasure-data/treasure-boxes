select
  rowid
  ,array_concat(
    quantitative_features(
      array("crim","zn","indus","nox","rm","age","dis","tax","ptratio","b","lstat")
      ,crim,zn,indus,nox,rm,age,dis,tax,ptratio,b,lstat
    )
    ,categorical_features(
      array("chas","rad")
      ,chas,rad
    )
  ) as features
  ,medv as price
from
  ${target_table}
;