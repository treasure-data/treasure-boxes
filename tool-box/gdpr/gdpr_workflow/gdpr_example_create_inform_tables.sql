DROP TABLE IF EXISTS inform;
CREATE TABLE inform (
  key varchar,
  db varchar,
  tbl varchar,
  json varchar
);


DROP TABLE IF EXISTS tmp_inform;
CREATE TABLE tmp_inform (
  key varchar,
  db varchar,
  tbl varchar,
  json varchar
) 