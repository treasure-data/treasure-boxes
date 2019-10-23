#!/bin/sh

set -x

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

DB_NAME="sentiment"
TABLE_NAME1="movie_review_train"
TABLE_NAME2="movie_review_test"

CONF_PARAM=""

if td ${CONF_PARAM} table:show ${DB_NAME} ${TABLE_NAME1} > /dev/null && td ${CONF_PARAM} table:show ${DB_NAME} ${TABLE_NAME2} > /dev/null ; then
  echo "table ${DB_NAME}.${TABLE_NAME1} and ${DB_NAME}.${TABLE_NAME2} exist. Skip"
  exit 0
else
  echo "Create target table ${DB_NAME}.${TABLE_NAME1} and ${TABLE_NAME2}"
fi

curl http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz --create-dirs -o resources/aclImdb.tar.gz
cd resources
tar xf aclImdb.tar.gz
rm aclImdb.tar.gz
cd ..
python py_scripts/data.py
rm -rf resources/aclImdb

td ${CONF_PARAM} db:create ${DB_NAME}
td ${CONF_PARAM} table:create ${DB_NAME} ${TABLE_NAME1}
td ${CONF_PARAM} import:auto \
  --format csv \
  --column-header \
  --column-types string,int,int \
  --time-value `date +%s` \
  --auto-create ${DB_NAME}.${TABLE_NAME1} ./resources/train.csv
td ${CONF_PARAM} table:create ${DB_NAME} ${TABLE_NAME2}
td ${CONF_PARAM} import:auto \
  --format csv \
  --column-header \
  --column-types string,int,int \
  --time-value `date +%s` \
  --auto-create ${DB_NAME}.${TABLE_NAME2} ./resources/test.csv

rm -rf out
rm resources/*
