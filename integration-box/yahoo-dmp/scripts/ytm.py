#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytd
from pytd.dbapi import connect
import requests


def fetch_row(sql, connection):
    cur = connection.cursor()
    cur.execute(sql)
    index = 0
    while True:
        row = cur.fetchone()
        if row is None:
            break
        yield index, row[0]
        index += 1


def call_api(sql, url, replaced_param):

    print("Reading sqlfile: {}".format(sql))
    f = open(sql, "r")
    sqlcontent = f.read()
    f.close

    print("SQL content is:")
    print(sqlcontent)

    client = pytd.Client(
        apikey=os.environ.get("td_apikey"),
        endpoint=os.environ.get("td_endpoint"),
        database=os.environ.get("td_database"),
        default_engine=os.environ.get("td_engine"),
    )
    conn = connect(client)

    print("API call start:")
    for index, row in fetch_row(sqlcontent, conn):
        u = url.replace(replaced_param, row)
        print(index, u)
        r = requests.get(u)
        print(r)

    print("API call finished")
