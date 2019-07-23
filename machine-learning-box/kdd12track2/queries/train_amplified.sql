WITH amplified as (
  select 
    features, label
  from (
    select
       amplify(${amplify_factor}, features, label) as (features, label)
    from  
       kddcup_train
  ) t
  CLUSTER BY rand(1) -- shuffle in random
)
-- DIGDAG_INSERT_LINE
select 
  feature,
  avg(weight) as weight
from (
  select 
     logress(features, label) as (feature,weight)
  from 
     amplified
) t 
group by feature
;
