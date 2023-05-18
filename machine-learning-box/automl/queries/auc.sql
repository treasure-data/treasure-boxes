-- DIGDAG_INSERT_LINE
select
  auc(prob, label) as auc
from (
  select predicted_proba as prob, ${target_column} as label
  from ${table}
  ORDER BY prob DESC
) t
