
import requests
import pandas as pd
import pytd
import os
import json

def get_all_parent_segment(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    data = res.json()['data']
    for d in data:
        for k in d.keys():
            if type(d[k]) is dict:
                d[k] = json.dumps(d[k])
    
    return data

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', cdp_api_endpoint='api-cdp.treasuredata.com'):
    url = 'https://%s/entities/parent_segments' % cdp_api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_parent_segment(url, headers)
    if len(l) == 0:
      print('no import record')
      return
    df = pd.DataFrame(l)
    df['time'] = int(session_unixtime)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
