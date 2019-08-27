-- DIGDAG_INSERT_LINE
SELECT
    l.userid,
    l.features,
    r.gender_age,
    -- random sampling
    rand(42) as rnd,
    -- stratified sampling
    count(1) over (partition by r.gender_age) as per_label_count,
    rank() over (partition by r.gender_age order by rand(41)) as rank_in_label
FROM
    features l
    LEFT OUTER JOIN gender_age r ON (l.userid = r.userid)
CLUSTER BY rand(43) -- random shuffling with random seed
