INSERT INTO TABLE tmp_inform
SELECT
${td.each.foreign_key} as key,
'${td.each.foreign_db}' as db,
'${td.each.foreign_table}' as tbl,
v as json
FROM ${td.each.foreign_db}.${td.each.foreign_table}
WHERE ${td.each.foreign_table}.${td.each.foreign_key} IN (SELECT foreign_key FROM tmp_inform_foreign_keys);