# https://api-docs.treasuredata.com/en/api/system-api/bulk-loads-api/

import requests
import pandas as pd
import pytd
import os
import json

def convert(s):
  return json.dumps(s)

def get_all_sources(url, headers):
  print(url)
  res = requests.get(url=url, headers=headers)
  if res.status_code != requests.codes.ok:
    res.raise_for_status()
  return res.json()

def run(dest_db, dest_table, api_endpoint='api.treasuredata.com'):
  url = 'https://%s/v3/bulk_loads/' % api_endpoint
  headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
  l = get_all_sources(url, headers)
  if len(l) == 0:
    print('no import record')
    return
  df = pd.DataFrame(l)
  df['config'] = df['config'].apply(convert)
  df['config_diff'] = df['config_diff'].apply(convert)
  client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
  client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
