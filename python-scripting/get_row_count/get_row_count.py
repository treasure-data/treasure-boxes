#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script get row count numbers from all tables of all databases,
# and import the result to specified db/table.

import sys
import os
import os.path
import time

import pytd
import pandas as pd

TD_APIKEY=os.environ.get('td_apikey')
DEST_DB='DB_NAME'
DEST_TABLE='TABLE_NAME'

#import pdb;pdb.set_trace()
def get_row_count():
  df = pd.DataFrame( columns=['db_name','table_name','row_count'] )
  client = pytd.Client(apikey=TD_APIKEY, endpoint='https://api.treasuredata.com/', database=DEST_DB, engine='presto')
  for db in client.list_databases():
    for table in client.list_tables(db.name):
      tmp_se = pd.Series( [ db.name, table.name, table.count ], index=df.columns )
      df = df.append( tmp_se, ignore_index=True )
      #print(db.name + ',' + table.name + ',' + str(table.count))
  #print(df)
  client.load_table_from_dataframe(df, DEST_TABLE, if_exists='append')
