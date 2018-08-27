select
  -- carrying over min-max of training data from "last_results"
  ${td.last_results. training_min_crim} as  training_min_crim, ${td.last_results.training_max_crim} as training_max_crim
  ,${td.last_results. training_min_zn} as  training_min_zn, ${td.last_results.training_max_zn} as training_max_zn
  ,${td.last_results. training_min_indus} as  training_min_indus, ${td.last_results.training_max_indus} as training_max_indus
  ,${td.last_results. training_min_chas} as  training_min_chas, ${td.last_results.training_max_chas} as training_max_chas
  ,${td.last_results. training_min_nox} as  training_min_nox, ${td.last_results.training_max_nox} as training_max_nox
  ,${td.last_results. training_min_rm} as  training_min_rm, ${td.last_results.training_max_rm} as training_max_rm
  ,${td.last_results. training_min_age} as  training_min_age, ${td.last_results.training_max_age} as training_max_age
  ,${td.last_results. training_min_dis} as  training_min_dis, ${td.last_results.training_max_dis} as training_max_dis
  ,${td.last_results. training_min_rad} as  training_min_rad, ${td.last_results.training_max_rad} as training_max_rad
  ,${td.last_results. training_min_tax} as  training_min_tax, ${td.last_results.training_max_tax} as training_max_tax
  ,${td.last_results. training_min_ptratio} as  training_min_ptratio, ${td.last_results.training_max_ptratio} as training_max_ptratio
  ,${td.last_results. training_min_b} as  training_min_b, ${td.last_results.training_max_b} as training_max_b
  ,${td.last_results. training_min_lstat} as  training_min_lstat, ${td.last_results.training_max_lstat} as training_max_lstat

  -- min-max for testing requires min-max all data; training & testing data set
  ,least(min(crim), ${td.last_results.training_min_crim}) as test_min_crim, greatest(max(crim), ${td.last_results.training_max_crim}) as test_max_crim
  ,least(min(zn), ${td.last_results.training_min_zn}) as test_min_zn, greatest(max(zn), ${td.last_results.training_max_zn}) as test_max_zn
  ,least(min(indus), ${td.last_results.training_min_indus}) as test_min_indus, greatest(max(indus), ${td.last_results.training_max_indus}) as test_max_indus
  ,least(min(chas), ${td.last_results.training_min_chas}) as test_min_chas, greatest(max(chas), ${td.last_results.training_max_chas}) as test_max_chas
  ,least(min(nox), ${td.last_results.training_min_nox}) as test_min_nox, greatest(max(nox), ${td.last_results.training_max_nox}) as test_max_nox
  ,least(min(rm), ${td.last_results.training_min_rm}) as test_min_rm, greatest(max(rm), ${td.last_results.training_max_rm}) as test_max_rm
  ,least(min(age), ${td.last_results.training_min_age}) as test_min_age, greatest(max(age), ${td.last_results.training_max_age}) as test_max_age
  ,least(min(dis), ${td.last_results.training_min_dis}) as test_min_dis, greatest(max(dis), ${td.last_results.training_max_dis}) as test_max_dis
  ,least(min(rad), ${td.last_results.training_min_rad}) as test_min_rad, greatest(max(rad), ${td.last_results.training_max_rad}) as test_max_rad
  ,least(min(tax), ${td.last_results.training_min_tax}) as test_min_tax, greatest(max(tax), ${td.last_results.training_max_tax}) as test_max_tax
  ,least(min(ptratio), ${td.last_results.training_min_ptratio}) as test_min_ptratio, greatest(max(ptratio), ${td.last_results.training_max_ptratio}) as test_max_ptratio
  ,least(min(b), ${td.last_results.training_min_b}) as test_min_b, greatest(max(b), ${td.last_results.training_max_b}) as test_max_b
  ,least(min(lstat), ${td.last_results.training_min_lstat}) as test_min_lstat, greatest(max(lstat), ${td.last_results.training_max_lstat}) as test_max_lstat
from
  ${source}_test