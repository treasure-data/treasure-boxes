DROP TABLE IF EXISTS gdpr_example_db.${td.param_table};
CREATE TABLE gdpr_example_db.${td.param_table} AS
SELECT
  json_extract_scalar(json_parse(${td.param_table}), '$.email') as email,
  json_extract_scalar(json_parse(${td.param_table}), '$.operation') as operation
-- perhaps add and use these below if/when operation is 'update'
  --json_extract_scalar(json_parse(${td.param_table}), '$.column') as operation 
  --json_extract_scalar(json_parse(${td.param_table}), '$.current_value') as operation
  --json_extract_scalar(json_parse(${td.param_table}), '$.update_value') as operation
FROM gdpr_example_db.json