#!/bin/sh

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

curl -o ml-1m.zip -L http://files.grouplens.org/datasets/movielens/ml-1m.zip
unzip ml-1m.zip
cd ml-1m
sed 's/::/,/g' ratings.dat > ratings.csv

td db:create movielens
td table:create movielens ratings
td import:auto \
  --format csv \
  --columns userid,itemid,rating,timestamp \
  --column-types long,long,double,long \
  --time-value `date +%s` \
  --auto-create movielens.ratings ./ratings.csv

cd ..
rm ml-1m.zip
rm -rf ml-1m
