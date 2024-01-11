# https://github.com/treasure-data/digdag/blob/master/digdag-server/src/main/java/io/digdag/server/rs/WorkflowResource.java#L109

import requests
import pandas as pd
import pytd
import os
import json

def convert_to_json(s):
  return json.dumps(s)

def get_workflows1(url, headers):
    print(url)
    res = requests.get(url=url, headers= headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    return res.json()['workflows']

def get_all_workflow(base_url, headers, count):
    wfs_list = list()

    url = base_url % (count, '0')
    wfs = get_workflows1(url, headers)

    while len(wfs) == count:
        wfs_list.extend(wfs)
        url = base_url % (count, wfs[-1]['id'])
        wfs = get_workflows1(url, headers)
    
    wfs_list.extend(wfs)
    return wfs_list

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com', count=100):
    workflow_url = 'https://%s/api/workflows' % workflow_endpoint + '?count=%d&last_id=%s'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    wfs_list = get_all_workflow(workflow_url, headers, count)
    df = pd.DataFrame(wfs_list)
    df['time'] = session_unixtime
    df['project'] = df['project'].apply(convert_to_json)
    df['config'] = df['config'].apply(convert_to_json)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')