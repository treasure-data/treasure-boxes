select
  min(i1) as train_min1, max(i1) as train_max1,
  min(i2) as train_min2, max(i2) as train_max2,
  min(i3) as train_min3, max(i3) as train_max3,
  min(i4) as train_min4, max(i4) as train_max4,
  min(i5) as train_min5, max(i5) as train_max5,
  min(i6) as train_min6, max(i6) as train_max6,
  min(i7) as train_min7, max(i7) as train_max7,
  min(i8) as train_min8, max(i8) as train_max8,
  min(i9) as train_min9, max(i9) as train_max9,
  min(i10) as train_min10, max(i10) as train_max10,
  min(i11) as train_min11, max(i11) as train_max11,
  min(i12) as train_min12, max(i12) as train_max12,
  min(i13) as train_min13, max(i13) as train_max13
from
  samples_train
;
