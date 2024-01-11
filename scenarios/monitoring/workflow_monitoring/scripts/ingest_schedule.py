# https://github.com/treasure-data/digdag/blob/master/digdag-server/src/main/java/io/digdag/server/rs/ScheduleResource.java#L85

import requests
import pandas as pd
import pytd
import os
import json

def convert_to_json(s):
  return json.dumps(s)

def get_schedules1(url, headers):
    print(url)
    res = requests.get(url=url, headers= headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    return res.json()['schedules']

def get_all_schedule(base_url, headers):
    sche_list = list()

    url = base_url % ('0')
    sches = get_schedules1(url, headers)

    while len(sches) == 100:
        sche_list.extend(sches)
        url = base_url % (sches[-1]['id'])
        sches = get_schedules1(url, headers)
    
    sche_list.extend(sches)
    return sche_list

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com'):
    workflow_url = 'https://%s/api/schedules' % workflow_endpoint + '?last_id=%s'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    sches_list = get_all_schedule(workflow_url, headers)
    df = pd.DataFrame(sches_list)
    df['time'] = int(session_unixtime)
    df['project'] = df['project'].apply(convert_to_json)
    df['workflow'] = df['workflow'].apply(convert_to_json)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')