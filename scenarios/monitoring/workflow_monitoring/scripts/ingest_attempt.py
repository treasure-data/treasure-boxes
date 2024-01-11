# https://github.com/treasure-data/digdag/blob/master/digdag-server/src/main/java/io/digdag/server/rs/AttemptResource.java#L100

import requests
import pandas as pd
import pytd
import os
from datetime import datetime as dt
import json

def convert(s):
  return int(dt.strptime(s, '%Y-%m-%dT%H:%M:%SZ').timestamp())

def convert_to_json(s):
  return json.dumps(s)

def get_attempt1(url, headers):
    print(url)
    res = requests.get(url=url, headers= headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    return res.json()['attempts']

def get_all_attempt(base_url, headers, count, lower_limit_attempt_id):
    atmp_list = list()

    url = base_url % (count)
    atmp = get_attempt1(url, headers)

    while len(atmp) == count and (int(atmp[-1]['id']) > int(lower_limit_attempt_id)):
        atmp_list.extend(atmp)
        url = (base_url + '&last_id=%s') % (count, atmp[-1]['id'])
        atmp = get_attempt1(url, headers)
    
    atmp_list.extend(atmp)
    return atmp_list

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com', count=100, lower_limit_attempt_id='9999999999', if_exists='append'):
    workflow_url = 'https://%s/api/attempts' % workflow_endpoint + '?page_size=%d&include_retried=true'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    atmp_list = get_all_attempt(workflow_url, headers, count, lower_limit_attempt_id)
    if len(atmp_list) == 0:
      print('no import record')
      return
    df = pd.DataFrame(atmp_list)
    df['time'] = df['createdAt'].apply(convert)
    df['id'] = df['id'].astype('int')
    df['project'] = df['project'].apply(convert_to_json)
    df['workflow'] = df['workflow'].apply(convert_to_json)
    df['params'] = df['params'].apply(convert_to_json)
    df = df[df['id'] > int(lower_limit_attempt_id)]
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists=if_exists, fmt='msgpack')