DELETE FROM ${marketo.type[i]}_dedup
WHERE TD_TIME_RANGE(time, '${marketo.from_date}', null, 'JST')
AND ${marketo.dedup_key[i]}	in (
  SELECT DISTINCT ${marketo.dedup_key[i]} FROM ${marketo.type[i]}
  WHERE TD_TIME_RANGE(time, '${marketo.from_date}', null, 'JST')
)
