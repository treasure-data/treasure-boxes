#!/bin/sh

set -x

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

DB_NAME="movielens"
TABLE_NAME="ratings"

if td table:show ${DB_NAME} ${TABLE_NAME} > /dev/null ; then
  echo "table ${DB_NAME}.${TABLE_NAME} exists. Skip"
  exit 0
else
  echo "Create target table ${DB_NAME}.${TABLE_NAME}"
fi

curl -o ml-1m.zip -L http://files.grouplens.org/datasets/movielens/ml-1m.zip
unzip ml-1m.zip
cd ml-1m
sed 's/::/,/g' ratings.dat > ratings.csv

td db:create ${DB_NAME}
td table:create ${DB_NAME} ${TABLE_NAME}
td import:auto \
  --format csv \
  --columns userid,itemid,rating,timestamp \
  --column-types long,long,double,long \
  --time-value `date +%s` \
  --auto-create ${DB_NAME}.${TABLE_NAME} ./ratings.csv

cd ..
rm ml-1m.zip
rm -rf ml-1m
