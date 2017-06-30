#!/bin/sh

td --apikey $TD_API_KEY import:auto \
  --format csv \
  --columns domain \
  --column-types string \
  --time-value `date +%s` \
  --auto-create ${target}.free_domain \
  ./resources/free.txt
