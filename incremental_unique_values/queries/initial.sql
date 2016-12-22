CREATE TABLE IF NOT EXISTS ${td.dest_db}.${td.dest_table}
AS SELECT DISTINCT(${td.target_field}) FROM ${td.source_table}
