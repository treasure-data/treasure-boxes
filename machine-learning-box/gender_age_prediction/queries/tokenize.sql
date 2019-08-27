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
  	tokenize_ja(
	  normalize_unicode(
        translate(contents,":","\;"),
		'NFKC'
      ),
      'normal',
      null, -- stopwords
      -- stoptags
      array("副詞","助詞","動詞","記号","名詞-数","副詞-一般","助詞-特殊","動詞-接尾","動詞-自立","名詞-接尾","名詞-特殊","記号-一般","記号-句点","記号-空白","記号-読点","名詞-接尾-一般","名詞-接尾-人名","名詞-接尾-地域","名詞-接尾-特殊","名詞-接尾-助数詞","名詞-接尾-サ変接続","名詞-接尾-副詞可能","名詞-接尾-助動詞語幹","名詞-特殊-助動詞語幹","名詞-接尾-形容動詞語幹","助詞-係助詞","助詞-副助詞","助詞-副詞化","助詞-格助詞","助詞-終助詞","助詞-連体化","動詞-非自立","名詞-代名詞","名詞-非自立","記号-括弧閉","記号-括弧開","助詞-格助詞-一般","助詞-格助詞-引用","助詞-格助詞-連語","名詞-代名詞-一般","名詞-代名詞-縮約","名詞-非自立-一般","名詞-非自立-副詞可能","名詞-非自立-助動詞語幹","名詞-非自立-形容動詞語幹","助詞-並立助詞","助詞-接続助詞","助詞-間投助詞","名詞-サ変接続","名詞-副詞可能","名詞-接続詞的","名詞-固有名詞-人名-名","名詞-固有名詞-人名-姓","副詞-助詞類接続","名詞-引用文字列","名詞-動詞非自立的","名詞-形容動詞語幹","名詞-ナイ形容詞語幹","記号-アルファベット","助詞-副助詞／並立助詞／終助詞","助動詞","形容詞","感動詞","接続詞","接頭詞","連体詞","その他-間投","形容詞-接尾","形容詞-自立","形容詞-非自立","接頭詞-数接続","接頭詞-動詞接続","接頭詞-名詞接続","接頭詞-形容詞接続","フィラー","非言語音"),
	  'https://s3.amazonaws.com/td-hivemall/dist/kuromoji-user-dict-neologd.csv.gz'
	)
  ) r as word
WHERE
  NOT is_stopword(r.word) AND
  length(r.word) >= 2 AND cast(r.word AS double) IS NULL