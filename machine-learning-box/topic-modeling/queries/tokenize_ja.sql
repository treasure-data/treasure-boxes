WITH exploded as (
  select
    t1.docid,
    t2.word
  from
    ${source} t1 LATERAL VIEW explode(
      tokenize_ja(
        normalize_unicode(contents,'NFKC'), -- unicode normalization
	    "normal",
	    -- stopwords
	    array("a","about","above","across","after","again","against","all","almost","alone","along","already","also","although","always","am","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","below","best","better","between","big","both","but","by","c","came","can","cannot","cars","case","cases","certain","certainly","clear","clearly","co","com","come","corp","could","d","did","differ","different","differently","do","does","doing","don","done","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","has","have","having","he","her","here","hers","herself","high","higher","highest","him","himself","his","how","however","http","https","i","id","if","important","in","inc","interest","interested","interesting","interests","into","is","it","its","itself","j","jp","just","k","keep","keeps","kind","kk","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","my","myself","n","necessary","need","needed","needing","needs","net","never","new","newer","newest","next","no","nobody","non","noone","nor","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","our","ours","ourselves","out","over","own","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","she","should","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","such","sure","t","take","taken","than","that","the","their","theirs","them","themselves","then","there","therefore","these","they","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","way","ways","we","well","wells","went","were","what","when","where","whether","which","while","who","whole","whom","whose","why","will","with","within","without","work","worked","working","works","would","www","x","y","year","years","yet","you","young","younger","youngest","your","yours","yourself","yourselves","z"),
        -- stoptags
	    array("副詞","助詞","動詞","記号","名詞-数","副詞-一般","助詞-特殊","動詞-接尾","動詞-自立","名詞-接尾","名詞-特殊","記号-一般","記号-句点","記号-空白","記号-読点","名詞-接尾-一般","名詞-接尾-人名","名詞-接尾-地域","名詞-接尾-特殊","名詞-接尾-助数詞","名詞-接尾-サ変接続","名詞-接尾-副詞可能","名詞-接尾-助動詞語幹","名詞-特殊-助動詞語幹","名詞-接尾-形容動詞語幹","助詞-係助詞","助詞-副助詞","助詞-副詞化","助詞-格助詞","助詞-終助詞","助詞-連体化","動詞-非自立","名詞-代名詞","名詞-非自立","記号-括弧閉","記号-括弧開","助詞-格助詞-一般","助詞-格助詞-引用","助詞-格助詞-連語","名詞-代名詞-一般","名詞-代名詞-縮約","名詞-非自立-一般","名詞-非自立-副詞可能","名詞-非自立-助動詞語幹","名詞-非自立-形容動詞語幹","助詞-並立助詞","助詞-接続助詞","助詞-間投助詞","名詞-サ変接続","名詞-副詞可能","名詞-接続詞的","名詞-固有名詞-人名-名","名詞-固有名詞-人名-姓","副詞-助詞類接続","名詞-引用文字列","名詞-動詞非自立的","名詞-形容動詞語幹","名詞-ナイ形容詞語幹","記号-アルファベット","助詞-副助詞／並立助詞／終助詞","助動詞","形容詞","感動詞","接続詞","接頭詞","連体詞","その他-間投","形容詞-接尾","形容詞-自立","形容詞-非自立","接頭詞-数接続","接頭詞-動詞接続","接頭詞-名詞接続","接頭詞-形容詞接続","フィラー","非言語音"),
	    "https://s3.amazonaws.com/td-hivemall/dist/kuromoji-user-dict-neologd.csv.gz"
      )
    ) t2 as word
)
-- DIGDAG_INSERT_LINE
select
  l.docid,
  l.word
from
  exploded l
where
  l.word NOT IN (select s.word from stopwords s) AND -- remove stopwords
  NOT is_stopword(l.word) AND
  length(l.word) >= 2 AND cast(l.word AS double) IS NULL -- trim number and single word
;
