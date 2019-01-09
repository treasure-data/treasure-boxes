select
  *
from
  ${source}_shuffled
-- ${train_sample_rate} can be configured in config.yml
-- You can use from 0.0 to 1.0
where
  rnd > ${train_sample_rate}
;
