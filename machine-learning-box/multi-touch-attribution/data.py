import os
import sys
import pandas as pd

os.system(f"{sys.executable} -m pip install -U pytd==1.0.0")


CSV_URL = 'https://gist.githubusercontent.com/takuti/c890cdcbae7946f21a0afc3a4d88ec9f/raw/8dae87e0ba4a258581f3be7ff52d16099eeceadd/touchpoints.csv'


def import_sample(database, table):
    import pytd

    apikey = os.environ['TD_API_KEY']
    apiserver = os.environ['TD_API_SERVER']
    client = pytd.Client(database=database, apikey=apikey, endpoint=apiserver)

    if client.exists(database, table):
        print('Target database and tables exists. Skip')
        return True

    df = pd.read_csv(CSV_URL)

    print('Upload sample data to Treasure Data')
    client.create_database_if_not_exists(database)
    client.load_table_from_dataframe(df, table, if_exists="overwrite")
