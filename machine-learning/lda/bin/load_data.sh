#!/bin/sh

SCRIPT_DIR=$(cd $(dirname $0); pwd)

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

wget https://github.com/myui/ml_dataset/raw/master/lda/lda_c.txt.gz
gunzip lda_c.txt.gz
mv lda_c.txt ${SCRIPT_DIR}/../.resources

td db:create lda
td table:create lda docs

td import:auto \
  --format tsv \
  --columns docid,contents \
  --column-types long,string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create lda.docs ${SCRIPT_DIR}/../.resources/lda_c.txt

td table:create lda stopwords
td import:auto \
  --format csv \
  --columns word \
  --column-types string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create lda.stopwords ${SCRIPT_DIR}/../.resources/stopwords.csv
