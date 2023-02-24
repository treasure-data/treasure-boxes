# https://api-docs.treasuredata.com/pages/td-api/tag/Connections/#tag/Connections/operation/getConnections

import requests
import pandas as pd
import pytd
import os

def get_all_connection(url, headers):
  print(url)
  res = requests.get(url=url, headers=headers)
  if res.status_code != requests.codes.ok:
    res.raise_for_status()
  return res.json()['results']

def run(dest_db, dest_table, api_endpoint='api.treasuredata.com'):
  url = 'https://%s/v3/result/list' % api_endpoint
  headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
  l = get_all_connection(url, headers)
  if len(l) == 0:
    print('no import record')
    return
  df = pd.DataFrame(l)
  client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
  client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
