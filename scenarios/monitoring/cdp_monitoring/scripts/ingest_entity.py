# https://api-docs.treasuredata.com/pages/audience_api_v1/tag/Parent-Segments/paths/~1audiences~1%7BaudienceId%7D~1folders/get/
# https://api-docs.treasuredata.com/pages/audience_api_v1/tag/Folders/paths/~1entities~1folders~1%7Bid%7D/get/

import requests
import pandas as pd
import pytd
import os
import json

def get_all_entities_per_folder(base_url, headers, folder_id):
    url = base_url + '/entities/by-folder/' + str(folder_id)
    print(url)
    l = []
    res = requests.get(url=url, headers=headers)
    if res.status_code != requests.codes.ok:
        #res.raise_for_status()
        return []
    data = res.json()['data']
    l.extend(data)
    for d in data:
        if d['type'] == 'folder-segment' and d['id'] != folder_id:
            ll = get_all_entities_per_folder(base_url, headers, d['id'])
            l.extend(ll)
    # dict => json
    for e in l:
        for k in e.keys():
            if type(e[k]) is dict:
                e[k] = json.dumps(e[k])
    return l

def get_all_entities(base_url, headers, root_ids):
    l = []
    for i in root_ids:
        l.extend(get_all_entities_per_folder(base_url, headers, i))

    return l

def run(session_unixtime, dest_db, dest_table, ids, api_endpoint='api.treasuredata.com', cdp_api_endpoint='api-cdp.treasuredata.com'):
    print('ingest entity record')
    if len(ids) == 0:
        print('no parent segment')
        return
    id_list = ids.split(',')
    if len(id_list) == 0:
        print('no parent segment')
        return
    print('count of parent segment: ' + str(len(id_list)))
    base_url = 'https://%s' % cdp_api_endpoint
    headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
    l = get_all_entities(base_url, headers, id_list)
    if len(l) == 0:
      print('no import record')
      return
    df = pd.DataFrame(l)
    df['time'] = int(session_unixtime)
    df = df.drop_duplicates(subset='id')
    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)
    client.load_table_from_dataframe(df, dest_table, if_exists='overwrite', fmt='msgpack')
