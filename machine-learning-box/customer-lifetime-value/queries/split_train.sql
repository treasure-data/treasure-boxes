select
  *
from
  cltv_shuffled
where
  rnd <= ${train_sample_rate}
