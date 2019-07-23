SELECT
  td_uid
  , ${map_cross_over[target].map_col_name}
  , MAX(last_access_time) AS last_access_time
  , ARRAY['${map_cross_over[target].cross_db}.${map_cross_over[target].cross_tbl}'] AS log_tbl_name
FROM
  ${map_cross_over[target].source_tbl} AS t1
  INNER JOIN (
    SELECT
      CAST(${map_cross_over[target].using_column} AS VARCHAR) AS ${map_cross_over[target].map_col_name}
      , ${map_cross_over[target].cross_key}
    FROM
      ${map_cross_over[target].cross_db}.${map_cross_over[target].cross_tbl}
    WHERE
      REGEXP_LIKE(CAST(${map_cross_over[target].using_column} AS VARCHAR), '${map_cross_over[target].reg_exp_validate}')
  ) AS t2 ON t1.${map_cross_over[target].source_key} = t2.${map_cross_over[target].cross_key}
GROUP BY
  td_uid
  , ${map_cross_over[target].map_col_name}
