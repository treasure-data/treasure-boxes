INSERT INTO tmp_unioned_segments

SELECT kuid, segment_name FROM ${td.each.table_name}