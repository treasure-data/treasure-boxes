-- @TD distribute_strategy: aggressive
WITH exploded as (
  SELECT
    userid,
    translate(r.word,':','\;') as word
  FROM
    blogposts l
    LATERAL VIEW explode(
      tokenize(normalize_unicode(translate(post,':','\;'),'NFKC'),true)
    ) r as word
  WHERE
    NOT is_stopword(r.word) AND
    length(r.word) >= 2 AND cast(r.word AS double) IS NULL
),
document_frequency AS (
  select
    word,
    count(distinct userid) docs
  from
    exploded
  group by
    word
  having   
    count(distinct userid) >= 2
),
wordcnt as (
  select
    l.userid,
    l.word,
    count(1) as cnt -- logscale count
  from
    exploded l
    LEFT SEMI JOIN document_frequency r ON (l.word = r.word)
  group by
    l.userid,
    l.word
),
ftvec as (
  select
    userid,
    to_ordered_list(feature(word,cnt), value, '-k 100') as features
  from
    wordcnt
  group by
    userid
),
ages as (
  select
    userid,
    (if(gender='male','M','F') ||
        CASE
           WHEN age >= 33 THEN '3x'
           WHEN age >= 23 THEN '2x'
           ELSE '1x'
        END
    ) as gender_age
  from
    blogposts
)
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
  ftvec l
  JOIN ages r ON (l.userid = r.userid)