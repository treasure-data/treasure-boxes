#!/bin/sh

set -ex

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

curl https://raw.githubusercontent.com/facebook/prophet/master/examples/example_retail_sales.csv --create-dirs -o ./resources/example_retail_sales.csv

td db:create timeseries
td table:create timeseries retail_sales
td import:auto \
    --format csv \
    --column-header \
    --column-types string,int \
    --time-value `date +%s` \
    --delimiter "," \
    --auto-create timeseries.retail_sales ./resources/example_retail_sales.csv

rm -rf out
rm resources/*
