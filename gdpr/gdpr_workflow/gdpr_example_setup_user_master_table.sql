DROP TABLE IF EXISTS gdpr_example_db.user_master;
CREATE TABLE gdpr_example_db.user_master AS
SELECT * FROM gdpr_example_db.user_master_source_data;