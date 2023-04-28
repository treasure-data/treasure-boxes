# https://docs.treasuredata.com/display/public/PD/Treasure+Data+Database+API
# <memo>
# ドキュメント上は/v3/database/listでidが得られるが実際は取れない
# /v3/database/show/:database_nameが必要 => こっちはdatatankというパラメータも取れる。
# ただし、ドキュメントは未記載

import requests
import pandas as pd
import pytd
import os

def get_all_database(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    # database id don't exist 
    return res.json()['databases']

def get_all_database_with_id(api_endpoint, headers, dbname_list):
    l = []
    for d in dbname_list:
        url = 'https://%s/v3/database/show/%s' % (api_endpoint, d['name'])
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        l.append(res.json())
    
    return l

def run(dest_db, dest_table, api_endpoint='api.treasuredata.com'):
    url = 'https://%s/v3/database/list' % api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    dbname_list = get_all_database(url, headers)
    if len(dbname_list) == 0:
        print('no import record')
        return
    db_list = get_all_database_with_id(api_endpoint, headers, dbname_list)
    df = pd.DataFrame(db_list)
    df = df.drop('permission', axis=1)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
