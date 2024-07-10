import requests
import pandas as pd
import pytd
import os
import json

def convert_to_json(s):
  return json.dumps(s)

def get_all_parent_segment_configuration(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    data = res.json()
    for d in data:
        for k in d.keys():
            if type(d[k]) is dict:
                d[k] = json.dumps(d[k])
    
    return data

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', cdp_api_endpoint='api-cdp.treasuredata.com'):
    url = 'https://%s/audiences' % cdp_api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_parent_segment_configuration(url, headers)
    if len(l) == 0:
      print('no import record')
      return
    df = pd.DataFrame(l)
    df['time'] = int(session_unixtime)
    df['attributes'] = df['attributes'].apply(convert_to_json)
    df['behaviors'] = df['behaviors'].apply(convert_to_json)

    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
