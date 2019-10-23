import io
import os
import shutil
import zipfile
from urllib.request import urlopen

import pandas as pd

os.system(f"{sys.executable} -m pip install -U pytd==0.8.0 td-client")

import pytd


def database_exists(database, client):
    from tdclient.errors import NotFoundError

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
    from tdclient.errors import NotFoundError

    try:
        client.api_client.table(database, table)
        return True
    except NotFoundError:
        pass

    return False


def upload_dataset(database, table):
    client = pytd.Client(
        apikey=os.environ["TD_API_KEY"], endpoint=os.environ["TD_API_SERVER"]
    )

    if database_exists(database, client) and table_exists(database, table, client):
        print("Target database and table exist. Skip")
        return True

    target_url = "http://files.grouplens.org/datasets/movielens/ml-1m.zip"
    fname = os.path.join("ml-1m", "ratings.dat")
    with urlopen(target_url) as res:
        info = res.info()
        if info.get_content_type() != "application/zip":
            raise IOError("Target file isn't Zip file. Might be corrupt")

        with zipfile.ZipFile(io.BytesIO(res.read())) as zipf:
            zipf.extract(fname)

    df = pd.read_csv(
        fname,
        sep="::",
        engine="python",
        names=["userid", "itemid", "rating", "timestamp"],
    )
    create_database_if_not_exists(database, client)
    client.load_table_from_dataframe(df, f"{database}.{table}", if_exists="overwrite")

    shutil.rmtree("ml-1m")
