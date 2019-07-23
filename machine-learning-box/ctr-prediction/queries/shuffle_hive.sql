select
  -- explicitly select all columns to exclude `v` column
  rowid, label,
  i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13,
  c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17,
  c18, c19, c20, c21, c22, c23, c24, c25, c26,
  -- stratified sampling
  count(1) over (partition by label) as per_label_count,
  rank() over (partition by label order by rand(41)) as rank_in_label
from
  ${source}
