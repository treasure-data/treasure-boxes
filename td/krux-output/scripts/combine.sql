SELECT td_global_id AS user_id,
       ARRAY_JOIN(ARRAY_DISTINCT(ARRAY_AGG(segment_name)), ',') AS td_segment
FROM tmp_unioned_segments GROUP BY td_global_id