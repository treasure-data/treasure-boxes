WITH userlog as (
  select
    td_client_id,
	COALESCE(td_description,td_title) as contents
  from
    tracking
  where
    TD_TIME_RANGE(
	  time,
	  TD_DATE_TRUNC('day', TD_TIME_ADD(TD_SCHEDULED_TIME(),'-${past_ndays}d','JST'), 'JST'),
	  null,
	  'JST'
    )
)
-- DIGDAG_INSERT_LINE
SELECT
  l.td_client_id as userid,
  translate(r.word,":","\;") as word
FROM
  userlog l
  LATERAL VIEW explode(
  	tokenize(
	  normalize_unicode(
	    translate(contents,":","\;"),
		'NFKC'
      ),
      true
	)
  ) r as word
WHERE
  NOT is_stopword(r.word) AND
  length(r.word) >= 2 AND cast(r.word AS double) IS NULL