cd stopwords

mkdir middle
cp stopwords.csv stop_words.csv
mv stop_words.csv middle
cd middle

td db:create stopwords
td table:create stopwords stopwords
td import:auto \
  --format csv \
  --columns word \
  --column-types string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create stopwords.stopwords ./stop_words.csv

cd ..
rm -rf middle

cd ..