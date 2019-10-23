import os

import pandas as pd


def upload_dataset(database, table):
    import pytd

    apikey = os.environ["TD_API_KEY"]
    apiserver = os.environ["TD_API_SERVER"]
    client = pytd.Client(database=database, apikey=apikey, endpoint=apiserver)

    if client.exists(database, table):
        print("Target database and table exist. Skip")
        return True

    fpath = os.path.join("resources", "boston_house_prices.csv")

    df = pd.read_csv(fpath)
    client.create_database_if_not_exists(database)
    client.load_table_from_dataframe(df, table, if_exists="overwrite")

    return True
