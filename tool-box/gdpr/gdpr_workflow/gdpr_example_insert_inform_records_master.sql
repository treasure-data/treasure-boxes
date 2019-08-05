INSERT INTO TABLE inform
SELECT
${td.each.fieldname} as key,
'${td.each.database}' as db,
'${td.each.table}' as tbl,
v as json
FROM ${td.each.database}.${td.each.table}
WHERE ${td.each.table}.${td.each.fieldname} IN (SELECT ${td.each.fieldname} from ${td.param_table} WHERE operation = 'INFORM');