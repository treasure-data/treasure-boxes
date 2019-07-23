import os, time, pandas, tdclient

os.system(f"{sys.executable} -m pip install -U pytd")

import pytd

TD_API_KEY = os.environ.get('td_apikey')
TD_API_SERVER = os.environ.get('td_endpoint')
TD_DATABASE = os.environ.get('td_database')
TD_TABLE = os.environ.get('td_table')


def get_job_list(status, max_num):
    with tdclient.Client(apikey=TD_API_KEY, endpoint=TD_API_SERVER) as client:
        data = []
        for job in client.jobs(0, max_num, status):
            job_detail = client.job(job.job_id)
            data.append({
                'time': int(time.time()),
                'job_id': str(job.job_id),
                'type': str(job_detail._type),
                'query': str(job_detail._query),
                'status': str(job_detail._status),
                'created_at': -1 if job_detail._created_at is None else int(job_detail._created_at.timestamp()),
                'start_at': -1 if job_detail._start_at is None else int(job_detail._start_at.timestamp()),
                'org_name': str(job_detail.org_name),
                'database': str(job_detail._database),
                'user_name': str(job_detail._user_name)
            })
        return data


def bulk_load(data):
    dataframe = pandas.DataFrame(
        columns=['time', 'job_id', 'type', 'query', 'status', 'created_at', 'start_at', 'org_name',
                 'database', 'user_name'])
    for item in data:
        record = pandas.Series(
            [item['time'], item['job_id'], item['type'], item['query'], item['status'],
             item['created_at'], item['start_at'],
             item['org_name'], item['database'], item['user_name']], index=dataframe.columns)
        dataframe = dataframe.append(record, ignore_index=True)

    with pytd.Client(apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE) as client:
        client.load_table_from_dataframe(dataframe, TD_TABLE, if_exists='append')


def monitoring():
    data = []
    data.extend(get_job_list('queued', 512))
    data.extend(get_job_list('running', 512))
    records = len(data)
    if records > 0:
        bulk_load(data)
        print('processed ' + str(records) + ' records.')
    else:
        print('no records.')
