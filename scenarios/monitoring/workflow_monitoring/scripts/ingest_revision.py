import requests
import os
import pytd
import pandas as pd
import json

def get_revision_info(base_url, headers, ids):
    l = []
    for i in ids:
        url = base_url % i
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        revisions = res.json()['revisions']
        for r in revisions:
            r['projectid'] = i
        l.extend(revisions)
    return l

def insert_revision_info(import_unixtime, endpoint, apikey, dest_db, dest_table, revisions):
    df = pd.DataFrame(revisions)
    df['time'] = int(import_unixtime)
    df['userInfo'] = df['userInfo'].apply(json.dumps)
    client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='append', fmt='msgpack')

def run(session_unixtime, dest_db, dest_table, project_ids, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com'):
    id_list = project_ids.split(',')
    if len(id_list) == 0:
        print('no project id')
        return

    workflow_url = 'https://%s/api/projects' % workflow_endpoint + '/%s/revisions'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_revision_info(workflow_url, headers, id_list)
    if len(l) == 0:
        print('no insert record')
        return
    insert_revision_info(session_unixtime, 'https://%s' % api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, l)