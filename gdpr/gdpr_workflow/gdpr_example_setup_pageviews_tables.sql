DROP TABLE IF EXISTS gdpr_example_db.pageviews1;
CREATE TABLE gdpr_example_db.pageviews1 AS
SELECT * FROM gdpr_example_db.pageviews_source_data;

DROP TABLE IF EXISTS gdpr_example_db.pageviews2;
CREATE TABLE gdpr_example_db.pageviews2 AS
SELECT * FROM gdpr_example_db.pageviews_source_data;


