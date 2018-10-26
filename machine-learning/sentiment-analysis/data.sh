#!/bin/sh

set -ex

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

curl http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz --create-dirs -o resources/aclImdb_v1.tar.gz
cd resources
tar xf aclImdb_v1.tar.gz
rm aclImdb_v1.tar.gz
cd ..
python data.py
rm -rf resources/aclImdb

CONF_PARAM=""

td ${CONF_PARAM} db:create sentiment
td ${CONF_PARAM} table:create sentiment movie_review_train
td ${CONF_PARAM} import:auto \
  --format csv \
  --column-header \
  --column-types string,int,int \
  --time-value `date +%s` \
  --auto-create sentiment.movie_review_train ./resources/train.csv
td ${CONF_PARAM} table:create sentiment movie_review_test
td ${CONF_PARAM} import:auto \
  --format csv \
  --column-header \
  --column-types string,int,int \
  --time-value `date +%s` \
  --auto-create sentiment.movie_review_test ./resources/test.csv

rm -rf out
rm resources/*
