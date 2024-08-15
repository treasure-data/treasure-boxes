import requests
import pandas as pd
import pytd
import os
import json

def get_all_datamodels(url, headers):
    print('Retrieving datamodels: ' + url)
    res = requests.get(url=url, headers=headers)

    if res.status_code == requests.codes.ok:
        return res.json()

    if res.status_code == requests.codes.forbidden:
        print('ERROR: API key user does not have access to Insights API')
    
    res.raise_for_status()

def run(dest_db, dest_table, api_endpoint='api.treasuredata.com'):
    apikey = os.environ['TD_API_KEY']
    
    url = 'https://%s/reporting/datamodels' % api_endpoint
    headers = {'Authorization': 'TD1 %s' % apikey}

    datamodel_list = get_all_datamodels(url, headers)
    
    if len(datamodel_list) == 0:
        print('no import record')
        return
    
    df = pd.DataFrame(datamodel_list)
    
    client = pytd.Client(apikey=apikey, endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
