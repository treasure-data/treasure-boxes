import requests
import pandas as pd
import pytd
import os
from datetime import datetime as dt

def convert(s):
    return int(dt.strptime(s, '%Y-%m-%d %H:%M:%S %Z').timestamp())

def delete_job_info(endpoint, apikey, dest_db, dest_table, ids):
    str = ''
    for i in ids:
        str = str + i + ","
    sql = "delete from %s.%s where job_id in (%s)" % (dest_db, dest_table, str[0:-1])
    print(sql)
    client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db, default_engine='presto')
    client.query(sql)

def get_job_info(base_url, headers, ids):
    l = []
    for i in ids:
        url = base_url % i
        print(url)
        res = requests.get(url=url, headers=headers)
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
        l.append(res.json())
    return l

def insert_job_info(endpoint, apikey, dest_db, dest_table, jobs, import_unixtime):
    df = pd.DataFrame(jobs)
    df['time'] = df['created_at'].apply(convert)
    df['job_id'] = df['job_id'].astype('int')
    client = pytd.Client(apikey=apikey, endpoint=endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='append', fmt='msgpack')

def run(session_unixtime, dest_db, dest_table, ids, api_endpoint='api.treasuredata.com'):
    print('update old job status')
    if len(ids) == 0:
        print('no update record')
        return
    id_list = ids.split(',')
    if len(id_list) == 0:
        print('no update record')
        return
    
    delete_job_info(api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, id_list)

    url = 'https://%s/v3/job/show/' % api_endpoint + '%s'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_job_info(url, headers, id_list)
    if len(l) == 0:
        print('no update record')
        return
    insert_job_info('https://%s' % api_endpoint, os.environ['TD_API_KEY'], dest_db, dest_table, l, session_unixtime)