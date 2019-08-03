--fetch columns name of master table 
SELECT 
  array_join(
    array_remove(array_remove(column_name_array,'${td.each.fieldname}'),'time'),
    ','
  ) AS column_names
FROM (
    SELECT 
      array_agg(column_name) AS column_name_array
    FROM
      information_schema.columns
    WHERE
      table_schema = '${td.each.database}'
      AND table_name = '${td.each.table}'
  ) t1