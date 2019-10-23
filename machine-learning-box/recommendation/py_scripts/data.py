import io
import os
import shutil
import zipfile
from urllib.request import urlopen

import pandas as pd
import pytd


def upload_dataset(database, table):
    client = pytd.Client(
        database=database,
        apikey=os.environ["TD_API_KEY"],
        endpoint=os.environ["TD_API_SERVER"],
    )

    if client.exists(database, table):
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
    client.create_database_if_not_exists(database)
    client.load_table_from_dataframe(df, f"{database}.{table}", if_exists="overwrite")

    shutil.rmtree("ml-1m")
