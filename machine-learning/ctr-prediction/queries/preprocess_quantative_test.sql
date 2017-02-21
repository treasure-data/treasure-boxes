with test_nonzero as (
  select
    rowid,
    IF( i1 IS NULL, 0, i1) as i1,
    IF( i2 IS NULL, 0, i2) as i2,
    IF( i3 IS NULL, 0, i3) as i3,
    IF( i4 IS NULL, 0, i4) as i4,
    IF( i5 IS NULL, 0, i5) as i5,
    IF( i6 IS NULL, 0, i6) as i6,
    IF( i7 IS NULL, 0, i7) as i7,
    IF( i8 IS NULL, 0, i8) as i8,
    IF( i9 IS NULL, 0, i9) as i9,
    IF( i10 IS NULL, 0, i10) as i10,
    IF( i11 IS NULL, 0, i11) as i11,
    IF( i12 IS NULL, 0, i12) as i12,
    IF( i13 IS NULL, 0, i13) as i13
  from
    test
),
quantative as (
  select rowid, 16777217 + 1 as feature, i1 as value from test_nonzero
  union all
  select rowid, 16777217 + 2 as feature, i2 as value from test_nonzero
  union all
  select rowid, 16777217 + 3 as feature, i3 as value from test_nonzero
  union all
  select rowid, 16777217 + 4 as feature, i4 as value from test_nonzero
  union all
  select rowid, 16777217 + 5 as feature, i5 as value from test_nonzero
  union all
  select rowid, 16777217 + 6 as feature, i6 as value from test_nonzero
  union all
  select rowid, 16777217 + 7 as feature, i7 as value from test_nonzero
  union all
  select rowid, 16777217 + 8 as feature, i8 as value from test_nonzero
  union all
  select rowid, 16777217 + 9 as feature, i9 as value from test_nonzero
  union all
  select rowid, 16777217 + 10 as feature, i10 as value from test_nonzero
  union all
  select rowid, 16777217 + 11 as feature, i11 as value from test_nonzero
  union all
  select rowid, 16777217 + 12 as feature, i12 as value from test_nonzero
  union all
  select rowid, 16777217 + 13 as feature, i13 as value from test_nonzero
),
quantative_stats as (
  select
    feature,
    min(value) as min,
    max(value) as max
  from
    quantative
  group by
    feature
),
quantative_normalized as (
  select
    t1.rowid,
    collect_list(
      feature(
        t1.feature, rescale(t1.value, t2.min, t2.max)
      )
    ) as features
  from
    quantative t1
    JOIN quantative_stats t2 ON (t1.feature = t2.feature)
  group by
    t1.rowid
)
-- DIGDAG_INSERT_LINE
SELECT
  rowid, features
FROM
  quantative_normalized
;
