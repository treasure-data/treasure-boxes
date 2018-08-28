#!/bin/sh

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

td db:create boston
td table:create boston house_prices
td import:auto \
  --format csv \
  --column-header \
  --column-types double,double,double,int,double,double,double,double,int,int,double,double,double,double \
  --time-value `date +%s` \
  --delimiter "," \
  --auto-create boston.house_prices ./resources/boston_house_prices.csv
