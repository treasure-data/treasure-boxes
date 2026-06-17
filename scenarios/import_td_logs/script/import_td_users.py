import os
import sys
os.system(f"{sys.executable} -m pip install -U pandas requests pytd==1.3.0")
import pandas as pd
import pytd
import requests

td_apikey = os.getenv("TD_API_KEY")


def import_users(database, table, api_endpoint):
    # get users data
    headers = {'Authorization': 'TD1 {}'.format(td_apikey)}
    r = requests.get('{}/v3/user/list'.format(api_endpoint), headers=headers)

    # write users data
    df = pd.json_normalize(r.json(), record_path=['users'])
    client = pytd.Client(apikey=td_apikey, database=database)
    client.load_table_from_dataframe(
        df, table, writer='bulk_import', if_exists='overwrite')
