WITH joined as (
	select
	  rowid() as rowid,
	  t.*,  
	  u.gender, -- '1'  for male, '2' for female,  and '0'  for unknown. 
	  u.age,    -- '1'  for (0, 12],  '2' for (12, 18], '3' for (18, 24], '4'  for  (24, 30], '5' for (30,  40], and '6' for greater than 40. 
	  rescale(t.depth,${min_depth},${max_depth}) as depth2,
	  rescale(t.position,${min_pos},${max_pos}) as position2,
	  (t.impression - t.clicks) as noclicks
	from 
	  ${in_db}.training t 
	  LEFT OUTER JOIN ${in_db}.users u on (t.userid = u.userid)
),
binarized as (
	select
	  binarize_label(
		noclicks, -- negative
		clicks, -- positive
		displayurl,adid,advetiserid,depth2,position2,queryid,keywordid,titleid,descriptionid,userid,gender,age
	  ) as 
		(displayurl,adid,advetiserid,depth,position,queryid,keywordid,titleid,descriptionid,userid,gender,age,label)
	from
	  joined
)
-- DIGDAG_INSERT_LINE
select
  add_bias(feature_hashing(
   array_concat(
     categorical_features(
       array('displayurl','adid','advetiserid','queryid','keywordid','titleid','descriptionid','userid','gender','age'),
       displayurl,adid,advetiserid,queryid,keywordid,titleid,descriptionid,userid,gender,age
     ),
     quantitative_features(
       array('depth','position'),
       depth,position
     )
   )
  )) as features, 
  label
from
  binarized  
CLUSTER BY rand(1); -- shuffle