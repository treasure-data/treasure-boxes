SELECT
  l.userid,
  l.rnd,
  l.gender_age,
  feature_hashing(l.features) as features, 
  r.label_id as label
FROM
  input l
  JOIN label_mapping r ON (l.gender_age = r.label)

