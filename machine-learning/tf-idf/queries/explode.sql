select
  docid,
  word
from
  ${source} LATERAL VIEW explode(tokenize(contents,true)) t as word
