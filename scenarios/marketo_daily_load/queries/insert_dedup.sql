SELECT ${td.last_results.column_names}
FROM (
  SELECT
    ${td.last_results.column_names},
    row_number() over (partition by ${marketo.dedup_key[i]} ORDER BY mk_updatedat DESC) as rnk
  FROM ${marketo.type[i]}
  WHERE TD_TIME_RANGE(time, '${marketo.from_date}', null, 'JST')
) t1
WHERE rnk = 1
