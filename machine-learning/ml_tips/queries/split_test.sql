-- client: molehill/0.0.1
select
  *
from
  ${source}_shuffled
where
  rnd > ${train_sample_rate}
;
