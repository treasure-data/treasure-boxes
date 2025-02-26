select
  auc(prob, label) as auc
from (
  select predicted_proba as prob, if(cast(${target_column} as string)=="${positive_class}", 1, 0) as label
  from ${table}
  ORDER BY prob DESC
) t
