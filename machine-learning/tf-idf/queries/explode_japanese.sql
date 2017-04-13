select
  docid,
  word
from
  ${source} LATERAL VIEW explode(
    tokenize_ja( -- japanese tokenizer
      normalize_unicode(contents,'NFKC') -- unicode normalization
    )
  ) t as word
