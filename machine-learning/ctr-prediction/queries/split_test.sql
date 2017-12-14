select *
from samples_shuffled
where rank_in_label > (per_label_count * ${train_sample_rate})
