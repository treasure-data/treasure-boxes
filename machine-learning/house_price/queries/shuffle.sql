SELECT
  rowid() as rowid
  ,rand(31) as rnd
  ,crim
  ,zn
  ,indus
  ,chas
  ,nox
  ,rm
  ,age
  ,dis
  ,rad
  ,tax
  ,ptratio
  ,b
  ,lstat
  ,medv
FROM
  ${source}
;
