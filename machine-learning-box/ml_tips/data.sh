#!/bin/bash

set -x

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

TD_OPT=""

td ${TD_OPT} db:create ml_tips
td ${TD_OPT} table:create ml_tips titanic
td ${TD_OPT} import:auto \
  --format csv \
  --column-header \
  --column-types int,int,string,string,double,int,int,string,double,string,string,string,int,string \
  --time-value `date +%s` \
  --delimiter "," \
  --auto-create ml_tips.titanic ./resources/titanic3.csv
