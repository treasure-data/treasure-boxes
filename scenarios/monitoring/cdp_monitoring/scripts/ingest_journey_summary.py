import requests
import pandas as pd
import pytd
import os
import json

def get_journey_summary(base_url, headers, id):
    url = base_url + '/entities/journeys/' + str(id)
    print(url)
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        res.raise_for_status()
    data = res.json()['data']
    if data == None or len(data) == 0:
        return None

    for k in data:
        if type(data[k]) is dict:
            data[k] = json.dumps(data[k])
    data['journey_id'] = id
    
    return data

def get_all_journey_summary(base_url, headers, ids):
    l = []
    for i in ids:
        d = get_journey_summary(base_url, headers, i)
        if d != None:
            l.append(d)
    return l

def run(session_unixtime, dest_db, dest_table, journey_ids, api_endpoint='api.treasuredata.com', cdp_api_endpoint='api-cdp.treasuredata.com'):
    print('ingest journey summary')
    if len(journey_ids) == 0:
        print('no jouney id')
        return
    id_list = journey_ids.split(',')
    if len(id_list) == 0:
        print('no jouney id')
        return
    print('count of target jouney: ' + str(len(id_list)))
    base_url = 'https://%s' % cdp_api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_journey_summary(base_url, headers, id_list)
    if len(l) == 0:
        print('no import record')
        return
    df = pd.DataFrame(l)
    df['time'] = int(session_unixtime)
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
