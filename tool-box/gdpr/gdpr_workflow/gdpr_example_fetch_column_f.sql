--fetch columns name of foreign table 
SELECT 
  array_join(
    transform(array_remove(array_remove(column_name_array,'${td.each.master_fn_name}'),'time'),x->concat('A','.',x)),
    ','
  ) AS column_names
FROM (
    SELECT 
      array_agg(column_name) AS column_name_array
    FROM
      information_schema.columns
    WHERE
      table_schema = '${td.each.foreign_db}'
      AND table_name = '${td.each.foreign_table}'
  ) t1

 
