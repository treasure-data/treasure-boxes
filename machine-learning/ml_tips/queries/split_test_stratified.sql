select *
from ${source}_shuffled
-- ${train_sample_rate} can be configured in config.yml
-- You can use from 0.0 to 1.0
where rank_in_label > (per_label_count * ${train_sample_rate})
;
