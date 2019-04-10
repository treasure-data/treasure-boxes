-- client: molehill/0.0.1
select
  array_max(array[approx_distinct(embarked), approx_distinct(sex), approx_distinct(pclass)]) as max_categorical_cardinality
from
  ${source}
;
