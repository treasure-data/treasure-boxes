#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import time

import pandas as pd

os.system(f"{sys.executable} -m pip install -U pytd")

import pytd


TD_APIKEY=os.environ.get('td_apikey')
TD_ENDPOINT=os.environ.get('td_endpoint')

def get_row_count(dest_db: str, dest_table: str):
    df = pd.DataFrame( columns=['db_name','table_name','row_count'] )
    client = pytd.Client(apikey=TD_APIKEY, endpoint=TD_ENDPOINT, database=dest_db, engine='presto')
    for db in client.list_databases():
        for table in client.list_tables(db.name):
            tmp_se = pd.Series( [ db.name, table.name, table.count ], index=df.columns )
            df = df.append( tmp_se, ignore_index=True )
            #print(db.name + ',' + table.name + ',' + str(table.count))
    #print(df)
    client.load_table_from_dataframe(df, dest_table, if_exists='append')
