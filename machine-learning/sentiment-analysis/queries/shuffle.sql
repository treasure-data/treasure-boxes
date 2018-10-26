select
  rowid() as rowid
  , sentence
  , sentiment
  , polarity
from
  ${source}
CLUSTER BY rand(43)
;
