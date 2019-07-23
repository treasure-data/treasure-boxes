#!/bin/sh

td --apikey $TD_API_KEY import:auto \
  --format csv \
  --columns title,role,job \
  --column-header \
  --column-types string,string,string \
  --time-value `date +%s` \
  --auto-create ${target}.title_mapping \
  ./resources/title_mapping.csv
