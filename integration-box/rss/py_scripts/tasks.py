#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pandas as pd

os.system(f"{sys.executable} -m pip install feedparser")
os.system(f"{sys.executable} -m pip install -U pytd==1.0.0")

TD_APIKEY = os.environ.get("td_apikey")
TD_ENDPOINT = os.environ.get("td_endpoint")


def rss_import(dest_db: str, dest_table: str, rss_url_list):
    import pytd
    import feedparser

    posts = []
    for rss_url in rss_url_list:
        d = feedparser.parse(rss_url)
        for entry in d.entries:
            posts.append((entry.title, entry.description, entry.link))

    df = pd.DataFrame(posts, columns=["title", "description", "link"])
    client = pytd.Client(apikey=TD_APIKEY, endpoint=TD_ENDPOINT, database=dest_db)
    client.create_database_if_not_exists(dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists="append")
