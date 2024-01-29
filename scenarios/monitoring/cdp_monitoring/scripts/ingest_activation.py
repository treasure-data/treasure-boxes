import requests
import pandas as pd
import pytd
import os
import json

def get_activations_per_audience(base_url, headers, id):
    url = base_url % id
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    activations = res.json()
    for a in activations:
        a['ps_id'] = id
    return activations

def get_all_activations(base_url, headers, id_list):
    l = []
    for i in id_list:
        l.extend(get_activations_per_audience(base_url=base_url, headers=headers, id=i))
    return l

def insert_activations(import_unixtime, endpoint, apikey, dest_db, dest_table, activations):
    df = pd.DataFrame(activations)
    df['time'] = int(import_unixtime)
    df['columns'] = df['columns'].apply(json.dumps)
    df['connectorConfig'] = df['connectorConfig'].apply(json.dumps)
    df['createdBy'] = df['createdBy'].apply(json.dumps)
    df['updatedBy'] = df['updatedBy'].apply(json.dumps)
    df['executions'] = df['executions'].apply(json.dumps)
    df['notifyOn'] = df['notifyOn'].apply(json.dumps)
    df['emailRecipients'] = df['emailRecipients'].apply(json.dumps)
    client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')

def run(session_unixtime, dest_db, dest_table, ids, api_endpoint='api.treasuredata.com',  cdp_api_endpoint='api-cdp.treasuredata.com'):
    id_list = ids.split(',')
    if len(id_list) == 0:
        print('no parent id')
        return
    cdp_url = 'https://%s/audiences' % cdp_api_endpoint + '/%s/syndications'
    headers =  {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_activations(cdp_url, headers, id_list)
    insert_activations(session_unixtime, 'https://%s' % api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, l)
