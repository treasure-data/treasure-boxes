SELECT
  t1.td_uid AS leader
  , t2.td_uid AS follower
FROM
  ${create_unify_num[target].table_name} AS t1
  LEFT JOIN ${create_unify_num[target].table_name} AS t2 ON t1.${create_unify_num[target].column_name} = t2.${create_unify_num[target].column_name}
