select
  rowid
  ,array_concat(
    quantitative_features(
      array("crim","zn","indus","chas","nox","rm","age","dis","rad","tax","ptratio","b","lstat")
      ,crim,zn,indus,chas,nox,rm,age,dis,rad,tax,ptratio,b,lstat
    )
  ) as features
  ,medv as price
from
  ${target_table}
;