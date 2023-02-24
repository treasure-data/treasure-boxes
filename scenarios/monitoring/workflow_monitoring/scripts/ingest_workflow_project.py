# https://github.com/treasure-data/digdag/blob/master/digdag-server/src/main/java/io/digdag/server/rs/ProjectResource.java#L240

import requests
import pandas as pd
import pytd
import os

def get_workflow_projects1(url, headers):
    print(url)
    res = requests.get(url=url, headers= headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    
    return res.json()['projects']

def get_all_workflow_project(base_url, headers, count):
    prj_list = list()

    url = base_url % (count, '0')
    projects = get_workflow_projects1(url, headers)

    while len(projects) == count:
        prj_list.extend(projects)
        url = base_url % (count, projects[-1]['id'])
        projects = get_workflow_projects1(url, headers)
    
    prj_list.extend(projects)
    return prj_list

def run(session_unixtime, dest_db, dest_table, api_endpoint='api.treasuredata.com', workflow_endpoint='api-workflow.treasuredata.com', count=100):
    workflow_url = 'https://%s/api/projects' % workflow_endpoint + '?count=%d&last_id=%s'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    project_list = get_all_workflow_project(workflow_url, headers, count)
    df = pd.DataFrame(project_list)
    df['time'] = int(session_unixtime)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')