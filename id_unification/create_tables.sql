DROP TABLE IF EXISTS ${td.source_tbl}_unify_loop_0;
CREATE TABLE IF NOT EXISTS ${td.source_tbl}_unify_loop_0 as select 1;

DROP TABLE IF EXISTS ${td.source_tbl}_loop_steps;
CREATE TABLE IF NOT EXISTS ${td.source_tbl}_loop_steps as select '${td.source_tbl}' tbl_name, cast(now() as varchar) completed_at,count(1) rows from ${td.source_tbl};

DROP TABLE IF EXISTS ${td.source_tbl}_unified_id_sets;
CREATE TABLE IF NOT EXISTS ${td.source_tbl}_unified_id_sets as select 1;

DROP TABLE IF EXISTS ${td.source_tbl}_enriched;
CREATE TABLE IF NOT EXISTS ${td.source_tbl}_enriched as select 1;

DROP TABLE IF EXISTS ${td.source_tbl}_unified;
CREATE TABLE IF NOT EXISTS ${td.source_tbl}_unified as select 1;