import requests
import pandas as pd
import pytd
import os
from datetime import datetime as dt
import json

def convert(s):
    return int(dt.strptime(s, '%Y-%m-%dT%H:%M:%S%z').timestamp())

def convert_to_json(s):
  return json.dumps(s)

def delete_session_info(endpoint, apikey, dest_db, dest_table, ids):
  s = ''
  for i in ids:
    s = s + str(i) + ","
  sql = "delete from %s.%s where id in (%s)" % (dest_db, dest_table, s[0:-1])
  print(sql)
  client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db, default_engine='presto')
  client.query(sql)

def get_session_info(base_url, headers, ids):
  l = []
  for i in ids:
    url = base_url % i
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
      res.raise_for_status()
    l.append(res.json())
  return l

def insert_session_info(endpoint, apikey, dest_db, dest_table, sessions, import_unix_time):
  df = pd.DataFrame(sessions)
  df['time'] = df['sessionTime'].apply(convert)
  df['id'] = df['id'].astype('int')
  df['project'] = df['project'].apply(convert_to_json)
  df['workflow'] = df['workflow'].apply(convert_to_json)
  df['lastAttempt'] = df['lastAttempt'].apply(convert_to_json)
  client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db)
  client.load_table_from_dataframe(df, dest_table, if_exists='append', fmt='msgpack')

def run(session_unixtime, dest_db, dest_table, ids, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com'):
  print('update retry session')
  if len(ids) == 0:
    print('no update record')
    return
  id_list = ids.split(',')
  if len(id_list) == 0:
    print('no update record')
    return
  delete_session_info(api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, id_list)

  workflow_url = 'https://%s/api/sessions' % workflow_endpoint + '/%s'
  headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
  l = get_session_info(workflow_url, headers, id_list)
  if len(l) == 0:
      print('no update record')
      return
  insert_session_info('https://%s' % api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, l, session_unixtime)
