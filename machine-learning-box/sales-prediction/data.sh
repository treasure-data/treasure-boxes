#!/bin/sh

set -x

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

DB_NAME="timeseries"
TABLE_NAME="retail_sales"

if td table:show ${DB_NAME} ${TABLE_NAME} > /dev/null ; then
  echo "table ${DB_NAME}.${TABLE_NAME} exists. Skip"
  exit 0
else
  echo "Create target table ${DB_NAME}.${TABLE_NAME}"
fi

curl https://raw.githubusercontent.com/facebook/prophet/master/examples/example_retail_sales.csv --create-dirs -o ./resources/example_retail_sales.csv

td db:create ${DB_NAME}
td table:create ${DB_NAME} ${TABLE_NAME}
td import:auto \
    --format csv \
    --column-header \
    --column-types string,int \
    --time-value `date +%s` \
    --delimiter "," \
    --auto-create ${DB_NAME}.${TABLE_NAME} ./resources/example_retail_sales.csv

rm -rf out
rm resources/*
