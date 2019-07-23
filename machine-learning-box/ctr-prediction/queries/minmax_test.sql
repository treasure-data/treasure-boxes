select
  -- carrying over the previous "last_results" (= min-max for training)
  ${td.last_results.train_min1} as train_min1, ${td.last_results.train_max1} as train_max1,
  ${td.last_results.train_min2} as train_min2, ${td.last_results.train_max2} as train_max2,
  ${td.last_results.train_min3} as train_min3, ${td.last_results.train_max3} as train_max3,
  ${td.last_results.train_min4} as train_min4, ${td.last_results.train_max4} as train_max4,
  ${td.last_results.train_min5} as train_min5, ${td.last_results.train_max5} as train_max5,
  ${td.last_results.train_min6} as train_min6, ${td.last_results.train_max6} as train_max6,
  ${td.last_results.train_min7} as train_min7, ${td.last_results.train_max7} as train_max7,
  ${td.last_results.train_min8} as train_min8, ${td.last_results.train_max8} as train_max8,
  ${td.last_results.train_min9} as train_min9, ${td.last_results.train_max9} as train_max9,
  ${td.last_results.train_min10} as train_min10, ${td.last_results.train_max10} as train_max10,
  ${td.last_results.train_min11} as train_min11, ${td.last_results.train_max11} as train_max11,
  ${td.last_results.train_min12} as train_min12, ${td.last_results.train_max12} as train_max12,
  ${td.last_results.train_min13} as train_min13, ${td.last_results.train_max13} as train_max13,
  -- min-max for testing should be computed on all of observed samples (i.e., train + test samples)
  least(min(i1), ${td.last_results.train_min1}) as test_min1, greatest(max(i1), ${td.last_results.train_max1}) as test_max1,
  least(min(i2), ${td.last_results.train_min2}) as test_min2, greatest(max(i2), ${td.last_results.train_max2}) as test_max2,
  least(min(i3), ${td.last_results.train_min3}) as test_min3, greatest(max(i3), ${td.last_results.train_max3}) as test_max3,
  least(min(i4), ${td.last_results.train_min4}) as test_min4, greatest(max(i4), ${td.last_results.train_max4}) as test_max4,
  least(min(i5), ${td.last_results.train_min5}) as test_min5, greatest(max(i5), ${td.last_results.train_max5}) as test_max5,
  least(min(i6), ${td.last_results.train_min6}) as test_min6, greatest(max(i6), ${td.last_results.train_max6}) as test_max6,
  least(min(i7), ${td.last_results.train_min7}) as test_min7, greatest(max(i7), ${td.last_results.train_max7}) as test_max7,
  least(min(i8), ${td.last_results.train_min8}) as test_min8, greatest(max(i8), ${td.last_results.train_max8}) as test_max8,
  least(min(i9), ${td.last_results.train_min9}) as test_min9, greatest(max(i9), ${td.last_results.train_max9}) as test_max9,
  least(min(i10), ${td.last_results.train_min10}) as test_min10, greatest(max(i10), ${td.last_results.train_max10}) as test_max10,
  least(min(i11), ${td.last_results.train_min11}) as test_min11, greatest(max(i11), ${td.last_results.train_max11}) as test_max11,
  least(min(i12), ${td.last_results.train_min12}) as test_min12, greatest(max(i12), ${td.last_results.train_max12}) as test_max12,
  least(min(i13), ${td.last_results.train_min13}) as test_min13, greatest(max(i13), ${td.last_results.train_max13}) as test_max13
from
  samples_test
;
