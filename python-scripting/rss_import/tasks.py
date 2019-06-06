#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import time

os.system(f"{sys.executable} -m pip install --user feedparser")

import pytd
import pandas as pd
import feedparser

TD_APIKEY=os.environ.get('td_apikey')
DB='YOUR_DATABASE'
TABLE='YOUR_TABLE'
RSS_URL_LIST = ['https://www.vogue.co.jp/rss/vogue', 'https://feeds.dailyfeed.jp/feed/s/7/887.rss']

def rss_import():
  df = pd.DataFrame( columns=['title','description','link'] )
  ts = str(int(time.time()))
  for rss_url in RSS_URL_LIST:
    d = feedparser.parse(rss_url)
    for entry in d.entries:
      tmp_se = pd.Series( [ entry.title, entry.description, entry.link ], index=df.columns )
      df = df.append( tmp_se, ignore_index=True )
  #print(df)
  client = pytd.Client(apikey=TD_APIKEY, endpoint='https://api.treasuredata.com/', database=DB, engine='presto')
  client.load_table_from_dataframe(df, TABLE, if_exists='overwrite')
