#!/bin/sh

set -x

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

DB_NAME="boston"
TABLE_NAME="house_prices"

if td table:show ${DB_NAME} ${TABLE_NAME} > /dev/null ; then
  echo "table ${DB_NAME}.${TABLE_NAME} exists. Skip"
  exit 0
else
  echo "Create target table ${DB_NAME}.${TABLE_NAME}"
fi

td db:create ${DB_NAME}
td table:create ${DB_NAME} ${TABLE_NAME}
td import:auto \
  --format csv \
  --column-header \
  --column-types double,double,double,int,double,double,double,double,int,int,double,double,double,double \
  --time-value `date +%s` \
  --delimiter "," \
  --auto-create ${DB_NAME}.${TABLE_NAME} ./resources/boston_house_prices.csv
