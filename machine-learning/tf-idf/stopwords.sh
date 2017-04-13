td db:create stopwords
td table:create stopwords stopwords
td import:auto \
  --format csv \
  --columns word \
  --column-types string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create stopwords.stopwords ./resources/stopwords.csv
