select 
  count(distinct docid) as n_docs 
from
  ${source}
