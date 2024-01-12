# https://github.com/treasure-data/digdag/blob/master/digdag-server/src/main/java/io/digdag/server/rs/SessionResource.java#L78

import requests
import pandas as pd
import pytd
import os
from datetime import datetime as dt
import json

def convert(session_time):
    return int(dt.strptime(session_time, '%Y-%m-%dT%H:%M:%S%z').timestamp())

def convert_to_json(s):
  return json.dumps(s)

def get_sessions1(url, headers):
    print(url)
    res = requests.get(url=url, headers= headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    return res.json()['sessions']

def get_all_session(base_url, headers, count, lower_limit_session_id):
    ses_list = list()

    url = base_url % (count)
    ses = get_sessions1(url, headers)
    while len(ses) == count and (int(ses[-1]['id']) > int(lower_limit_session_id)):
        ses_list.extend(ses)
        url = (base_url + '&last_id=%s') % (count, ses[-1]['id'])
        ses = get_sessions1(url, headers)
    
    ses_list.extend(ses)
    return ses_list
    
def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com', count=100, lower_limit_session_id='9999999999', if_exists='append'):
    workflow_url = 'https://%s/api/sessions' % workflow_endpoint + '?page_size=%d'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    ses_list = get_all_session(workflow_url, headers, count, lower_limit_session_id)
    if len(ses_list) == 0:
      print('no import record')
      return
    df = pd.DataFrame(ses_list)
    df['time'] = df['sessionTime'].apply(convert)
    df['id'] = df['id'].astype('int')
    df['project'] = df['project'].apply(convert_to_json)
    df['workflow'] = df['workflow'].apply(convert_to_json)
    df['lastAttempt'] = df['lastAttempt'].apply(convert_to_json)
    df = df[df['id'] > int(lower_limit_session_id)]
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists=if_exists, fmt='msgpack')
