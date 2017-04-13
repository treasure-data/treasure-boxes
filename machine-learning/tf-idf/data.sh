#!/bin/sh

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

td db:create tfidf
td table:create tfidf docs
td import:auto \
  --format tsv \
  --columns docid,contents \
  --column-types long,string \
  --time-value `date +%s` \
  --delimiter "|" \
  --auto-create tfidf.docs ./resources/sample_docs.tsv
