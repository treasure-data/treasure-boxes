# https://api-docs.treasuredata.com/pages/td-api/tag/Jobs/#tag/Jobs/operation/getJobs
# https://docs.treasuredata.com/display/public/PD/Treasure+Data+Job+APIs#job-list
import requests
import pandas as pd
import pytd
import os
from datetime import datetime as dt

def convert(s):
    return int(dt.strptime(s, '%Y-%m-%d %H:%M:%S %Z').timestamp())

def get_job1(url, headers):
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    return res.json()['jobs']

def get_all_job(base_url, headers, page_size, lower_job_id):
    job_list = []
    from_value = 0
    to_value = from_value + page_size - 1
    url = base_url % (from_value, to_value)
    jobs = get_job1(url, headers)
    while len(jobs) == page_size and (int(jobs[-1]['job_id']) > int(lower_job_id)):
        job_list.extend(jobs)
        from_value = to_value + 1
        to_value = from_value + page_size -1
        url = base_url % (from_value, to_value)
        jobs = get_job1(url, headers)

    job_list.extend(jobs)
    return job_list

def run(session_unixtime, dest_db, dest_table, page_size=1000, lower_job_id=9999999999, api_endpoint='api.treasuredata.com', if_exists='append'):
    base_url = 'https://%s/v3/job/list' % api_endpoint + '?from=%d&to=%d'
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    job_list = get_all_job(base_url, headers, page_size, lower_job_id)
    if len(job_list) == 0:
        print('no import record')
        return

    df = pd.DataFrame(job_list)
    df['time'] = df['created_at'].apply(convert)
    df = df.drop_duplicates(subset='job_id')
    df['job_id'] = df['job_id'].astype('int')
    df = df[df['job_id'] > int(lower_job_id)]
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists=if_exists, fmt='msgpack')

