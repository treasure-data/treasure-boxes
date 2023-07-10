# https://docs.treasuredata.com/display/public/PD/Permission+Policy+API

import requests
import pandas as pd
import pytd
import os
import json

def get_all_policy(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    return res.json()

def get_all_policy_with_permission(api_endpoint, headers, policyid_list):
    l = []
    for i in policyid_list:
        url = 'https://%s/v3/access_control/policies/%d/permissions' % (api_endpoint, i)
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        permissions = res.json()
        permissions['id'] = i

        l.append(permissions)
    return l

def get_all_policy_with_column_permission(api_endpoint, headers, policyid_list):
    l = []
    for i in policyid_list:
        url = 'https://%s/v3/access_control/policies/%d/column_permissions' % (api_endpoint, i)
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        column_permissions = res.json()
        if len(column_permissions) != 0:
            data = {'id': i, 'column_permissions': json.dumps(column_permissions)}
            l.append(data)
    return l

def get_all_assign_users(api_endpoint, headers, policyid_list):
    l = []
    for i in policyid_list:
        url = 'https://%s/v3/access_control/policies/%s/users' % (api_endpoint, i)
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        assign_users = res.json()
        if len(assign_users) != 0:
            data = {'id': i, 'assign_users': json.dumps(assign_users)}
            l.append(data)
    return l

def run(dest_db, policy_table, policy_detail_table, policy_detail_column_permission_table, policy_assign_users_table, api_endpoint='api.treasuredata.com'):
    # get policy list
    url = 'https://%s/v3/access_control/policies' % api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    policy_list = get_all_policy(url, headers)
    if len(policy_list) == 0:
        print('no import record')
        return
    df = pd.DataFrame(policy_list)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, policy_table, if_exists='overwrite', fmt='msgpack')

    # get permissions per policy
    policy_permissions_list = get_all_policy_with_permission(api_endpoint, headers, df['id'])
    if len(policy_permissions_list) != 0:
        policy_permissions = pd.DataFrame(policy_permissions_list)
        client.load_table_from_dataframe(policy_permissions, policy_detail_table, if_exists='overwrite', fmt='msgpack')
    else:
        print('no import policy permission')

    # get column permissions per policy
    policy_column_permission_list = get_all_policy_with_column_permission(api_endpoint, headers, df['id'])
    if len(policy_column_permission_list) != 0:
        policy_column_permissions = pd.DataFrame(policy_column_permission_list)
        client.load_table_from_dataframe(policy_column_permissions, policy_detail_column_permission_table, if_exists='overwrite', fmt='msgpack')
    else:
        print('no import policy column permission')

    # get policy users
    # https://api-docs.treasuredata.com/pages/td-api/tag/Access-Control-Users/#tag/Access-Control-Users/operation/getAccessControlPolicyUsers
    policy_assign_users_list = get_all_assign_users(api_endpoint, headers, df['id'])
    if len(policy_assign_users_list) != 0:
        policy_assign_users = pd.DataFrame(policy_assign_users_list)
        client.load_table_from_dataframe(policy_assign_users, policy_assign_users_table, if_exists='overwrite', fmt='msgpack')
    else:
        print('no import policy assign users')



    

