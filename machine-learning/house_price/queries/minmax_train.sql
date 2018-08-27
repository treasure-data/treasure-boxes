select
  min(crim) as training_min_crim, max(crim) as training_max_crim
  ,min(zn) as training_min_zn, max(zn) as training_max_zn
  ,min(indus) as training_min_indus, max(indus) as training_max_indus
  ,min(chas) as training_min_chas, max(chas) as training_max_chas
  ,min(nox) as training_min_nox, max(nox) as training_max_nox
  ,min(rm) as training_min_rm, max(rm) as training_max_rm
  ,min(age) as training_min_age, max(age) as training_max_age
  ,min(dis) as training_min_dis, max(dis) as training_max_dis
  ,min(rad) as training_min_rad, max(rad) as training_max_rad
  ,min(tax) as training_min_tax, max(tax) as training_max_tax
  ,min(ptratio) as training_min_ptratio, max(ptratio) as training_max_ptratio
  ,min(b) as training_min_b, max(b) as training_max_b
  ,min(lstat) as training_min_lstat, max(lstat) as training_max_lstat
from
  ${source}_training
;
