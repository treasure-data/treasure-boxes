SELECT 
  array_join(
    column_name_array,
    ','
  ) AS column_names
FROM (
    SELECT 
      array_agg(column_name) AS column_name_array
    FROM
      information_schema.columns
    WHERE
      table_schema = '${td.dest_db}'
      AND table_name = '${marketo.type[i]}'
  ) t1
