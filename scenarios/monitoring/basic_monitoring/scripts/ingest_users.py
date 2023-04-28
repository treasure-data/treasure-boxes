# https://docs.treasuredata.com/display/public/PD/Treasure+Data+User+API
import requests
import pandas as pd
import pytd
import os
import json

def get_all_users(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    return res.json()['users']

def get_all_assign_policies(api_endpoint, headers, userid_list):
    l = []
    for i in userid_list:
        url = 'https://%s/v3/access_control/users/%d' %(api_endpoint, i)
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        assign_policies = res.json()
        if len(assign_policies) != 0:
            data = {'id': i, 'assign_policy': json.dumps(assign_policies)}
            l.append(data)
    return l

def run(dest_db, dest_table, user_assign_policies_table, api_endpoint='api.treasuredata.com'):
    # get users
    url = 'https://%s/v3/user/list' % api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_users(url, headers)
    if len(l) == 0:
        print('no import record')
        return
    df = pd.DataFrame(l)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')

    # get assign policies
    policies_per_user = get_all_assign_policies(api_endpoint, headers, df['id'])
    if len(policies_per_user) != 0:
        policies_per_user_df = pd.DataFrame(policies_per_user)
        client.load_table_from_dataframe(policies_per_user_df, user_assign_policies_table, if_exists='overwrite', fmt='msgpack')
    else:
        print('no import user assign policy')