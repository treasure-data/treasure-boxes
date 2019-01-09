select
  *
from
  ${source}_shuffled
where
  rnd <= ${train_sample_rate}
;
