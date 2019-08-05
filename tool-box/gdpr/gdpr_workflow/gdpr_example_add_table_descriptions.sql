CREATE TABLE tmp2_inform AS
SELECT
inform.key,
inform.db,
inform.tbl,
lookup.table_description,
inform.json
FROM inform 
LEFT JOIN pii_table_desc_lookup lookup ON lookup.db_name = inform.db AND lookup.table_name = inform.tbl;

DROP TABLE inform;

CREATE TABLE inform AS SELECT * FROM tmp2_inform;