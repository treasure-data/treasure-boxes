import os, sys, re, pandas, tdclient, json
from datetime import datetime as dt
from mapping import mapping as mp
from time import sleep

os.system(f"{sys.executable} -m pip install -U pytd")
os.system(f"{sys.executable} -m pip install TwitterSearch")

import pytd
from TwitterSearch import *

TD_API_KEY = os.environ.get('td_apikey')
TD_API_SERVER = os.environ.get('td_endpoint')
TD_DATABASE = os.environ.get('td_database')
TD_TABLE = os.environ.get('td_table')

TW_CONSUMER_KEY = os.environ.get('tw_consumer_key')
TW_CONSUMER_SECRET = os.environ.get('tw_consumer_secret')
TW_ACCESS_TOKEN = os.environ.get('tw_access_token')
TW_ACCESS_SECRET = os.environ.get('tw_access_token_secret')
TW_SEARCH_KEYWORD = os.environ.get('tw_search_keyword')


def get_since_id():
    query = 'SELECT MAX(id) id FROM {db}.{table}'.format(
        db=TD_DATABASE,
        table=TD_TABLE
    )
    with pytd.Client(apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE) as client:
        result = client.query(query)
    if type(result['data'][0][0]) is int:
        return int(result['data'][0][0])
    else:
        return 0


def format_timestamp(val):
    return '' if val is '' else int(dt.strptime(val, '%a %b %d %H:%M:%S %z %Y').timestamp())


def make_array(key, data):
    result = []
    for item in data:
        result.append(item.get(key))
    return str(json.dumps(result))


def nest_get(path, data):
    hier = path.split('.')
    result = ''
    for key in hier:
        if data.get(key) is not None:
            if key == 'hashtags' or key == 'symbols':
                result = make_array('text', data.get(key))
            elif key == 'urls':
                result = make_array('expanded_url', data.get(key))
            elif key == 'user_mentions':
                result = make_array('screen_name', data.get(key))
            else:
                result = data.get(key)
                data = result
    return result


def pick_primary_url(urls):
    urls = json.loads(urls)
    pattern = re.compile(r".*%s.*" % TW_SEARCH_KEYWORD)
    result = ''
    if len(urls) > 0:
        result = urls[0]
        for url in urls:
            if pattern.match(url):
                result = url
    return result


def bulk_load(data):
    dataframe = pandas.DataFrame(columns=mp.keys())
    for item in data:
        record = pandas.Series(list(item.values()), index=dataframe.columns)
        dataframe = dataframe.append(record, ignore_index=True)

    with pytd.Client(apikey=TD_API_KEY, endpoint=TD_API_SERVER, database=TD_DATABASE) as client:
        client.load_table_from_dataframe(dataframe, TD_TABLE, if_exists='append')


def search_and_archive():
    todo = True
    results = []
    next_max_id = 0
    since_id = get_since_id()

    tso = TwitterSearchOrder()
    tso.add_keyword(TW_SEARCH_KEYWORD)
    tso.set_result_type('recent')
    if since_id > 0:
        tso.set_since_id(since_id)

    ts = TwitterSearch(
        consumer_key=TW_CONSUMER_KEY,
        consumer_secret=TW_CONSUMER_SECRET,
        access_token=TW_ACCESS_TOKEN,
        access_token_secret=TW_ACCESS_SECRET
    )
    while (todo):
        print('Current MaxID is ' + str(next_max_id))
        response = ts.search_tweets(tso)
        todo = not len(response['content']['statuses']) == 0
        for tweet in response['content']['statuses']:
            result = {}
            for key in mp:
                result[key] = str(nest_get(mp[key], tweet))
            result.update({
                'time': format_timestamp(result['created_at']),
                'created_at': format_timestamp(result['created_at']),
                'rt_created_at': format_timestamp(result['rt_created_at']),
                'qs_created_at': format_timestamp(result['qs_created_at']),
                'primary_url': pick_primary_url(result['entities_urls']),
                'rt_primary_url': pick_primary_url(result['rt_entities_urls']),
                'qs_primary_url': pick_primary_url(result['qs_entities_urls']),
            })
            results.append(result)

            if (tweet['id'] < next_max_id) or (next_max_id == 0):
                next_max_id = tweet['id']
                next_max_id -= 1

        records = len(results)
        if records > 450 or todo is not True:
            bulk_load(results)
            results = []
            print('processed ' + str(records) + ' records.')

        tso.set_max_id(next_max_id)
        sleep(2)
