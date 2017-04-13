#!/bin/sh

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

mkdir middle
cd middle

curl -o tfidf_test.tsv -L https://gist.githubusercontent.com/myui/190b91a3a792ccfceda0/raw/327acd192da4f96da8276dcdff01b19947a4373c/tfidf_test.tsv

td db:create tfidf
td table:create tfidf wikipage
td import:auto \
  --format tsv \
  --columns docid,contents \
  --column-types long,string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create tfidf.wikipage ./tfidf_test.tsv

cd ..
rm -rf middle