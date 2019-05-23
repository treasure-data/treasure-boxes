INSERT INTO tmp_unioned_segments

SELECT td_global_id, segment_name FROM ${td.each.table_name}