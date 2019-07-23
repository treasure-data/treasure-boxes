#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import time

os.system(f"{sys.executable} -m pip install feedparser")
os.system(f"{sys.executable} -m pip install -U pytd")

import pytd
import pandas as pd
import feedparser

TD_APIKEY=os.environ.get('td_apikey')
TD_ENDPOINT=os.environ.get('td_endpoint')

def rss_import(dest_db: str, dest_table: str, rss_url_list):
    df = pd.DataFrame( columns=['title','description','link'] )
    ts = str(int(time.time()))
    for rss_url in rss_url_list:
        d = feedparser.parse(rss_url)
        for entry in d.entries:
            tmp_se = pd.Series( [ entry.title, entry.description, entry.link ], index=df.columns )
            df = df.append( tmp_se, ignore_index=True )
    #print(df)
    client = pytd.Client(apikey=TD_APIKEY, endpoint=TD_ENDPOINT, database=dest_db, engine='presto')
    client.load_table_from_dataframe(df, dest_table, if_exists='append')
