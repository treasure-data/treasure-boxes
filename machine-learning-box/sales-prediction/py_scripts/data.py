import os
import sys

import pandas as pd

os.system(f"{sys.executable} -m pip install -U pytd==0.8.0 td-client")

import pytd
from tdclient.errors import NotFoundError


def database_exists(database, client):

    try:
        client.api_client.database(database)
        return True
    except NotFoundError:
        pass

    return False


def create_database_if_not_exists(database, client):
    if database_exists(database, client):
        print(f"DB {database} already exists")
        return False
    else:
        client.api_client.create_database(database)
        print(f"Created DB: {database}")
        return True


def table_exists(database, table, client):
    try:
        client.api_client.table(database, table)
        return True
    except NotFoundError:
        pass

    return False


def upload_dataset(database, table):
    apikey = os.environ["TD_API_KEY"]
    apiserver = os.environ["TD_API_SERVER"]
    client = pytd.Client(apikey=apikey, endpoint=apiserver)

    if database_exists(database, client) and table_exists(database, table, client):
        print("Target database and table exist. Skip")
        return True

    target_url = "https://raw.githubusercontent.com/facebook/prophet/master/examples/example_retail_sales.csv"

    df = pd.read_csv(target_url)
    create_database_if_not_exists(database, client)
    client.load_table_from_dataframe(df, f"{database}.{table}", if_exists="overwrite")

    return True
