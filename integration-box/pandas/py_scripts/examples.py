# Because we do not allow custom image currently, this is how you can add 3rd party
# libraries instead
import os
import sys
import tdclient

os.system(f"{sys.executable} -m pip install -U pytd==1.0.0")

apikey = os.environ['TD_API_KEY']
apiserver = os.environ['TD_API_SERVER']

def read_td_table(database_name, table_name, engine_name='presto', limit=1000):
    import pytd
    import pandas as pd

    client = pytd.Client(apikey=apikey, endpoint=apiserver, database=database_name)

    res = client.query(f"select * from {table_name} limit {limit}", engine=engine_name)
    df = pd.DataFrame(**res)
    print(df)

def write_td_table(database_name, table_name):
    import pytd
    import pandas as pd
    import random

    client = pytd.Client(apikey=apikey, endpoint=apiserver, database=database_name)
    df = pd.DataFrame({"c":[random.random() for _ in range(20)]})

    client.create_database_if_not_exists(database_name)

    table_path = f"{database_name}.{table_name}"
    client.load_table_from_dataframe(df, table_path, if_exists="overwrite")
