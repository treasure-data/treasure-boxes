import requests
import pandas as pd
import pytd
import os

def get_connection_details(base_url, headers, name):
    url = base_url % name
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    return res.json()

def get_all_connection_details(base_url, headers, name_list):
    l = []
    for n in name_list:
        r = get_connection_details(base_url, headers, n)
        r['name'] = n
        l.append(r)
    return l

def run(dest_db, dest_table, names, api_endpoint='api.treasuredata.com'):
    url = 'https://%s/v3/connections/lookup' % api_endpoint + '?name=%s'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    name_list = names.split(',')
    if len(name_list) == 0:
        print('no name list')
        return
    connection_map = get_all_connection_details(base_url=url, headers=headers, name_list=name_list)
    if len(connection_map) == 0:
        print('no connection map')
        return
    print(connection_map)
    df = pd.DataFrame(connection_map)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
