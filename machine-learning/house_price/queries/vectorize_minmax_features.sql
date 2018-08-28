select
  rowid
  ,array_concat(
    -- Use top 4 correlated features, `lstat`, `rm`, `ptratio`, `indus`:
    quantitative_features(
      array("indus","rm","ptratio","lstat")
      ,rescale(
        indus
        ,${indus_min}
        ,${indus_max}
      )
      ,rescale(
        rm
        ,${rm_min}
        ,${rm_max}
      )
      ,rescale(
        ptratio
        ,${ptratio_min}
        ,${ptratio_max}
      )
      ,rescale(
        lstat
        ,${lstat_min}
        ,${lstat_max}
      )
    )
  ) as features
  ,medv as price
from
  ${target_table}
;