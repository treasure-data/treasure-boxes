INSERT INTO inform 
SELECT
tmp_inform_foreign_keys.master_key as key,
tmp_inform.db,
tmp_inform.tbl,
tmp_inform.json,
tmp_inform.time
FROM tmp_inform
LEFT JOIN tmp_inform_foreign_keys on tmp_inform.key = tmp_inform_foreign_keys.foreign_key;

DELETE FROM tmp_inform WHERE time IS NOT NULL;
