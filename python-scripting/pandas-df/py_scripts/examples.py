# Because we do not allow custom image currently, this is how you can add 3rd party
# libraries instead
import os
import tdclient

os.system(f"{sys.executable} -m pip install -U pytd")

import pytd.pandas_td as td

apikey = os.environ['TD_API_KEY']
endpoint = os.environ['TD_API_SERVER']

con = td.connect(apikey=apikey, endpoint=endpoint)

def read_td_table(database_name, table_name, engine_name = 'presto', limit=1000):
    engine = td.create_engine(f"{engine_name}:{database_name}", con=con)
    df = td.read_td(f'SELECT * FROM {table_name} LIMIT {limit}', engine)
    print(df)

def write_td_table(database_name, table_name):
    import pandas as pd
    import random
    # TODO TD client, check for table's existence
    engine = td.create_engine(f"presto:{database_name}", con=con)
    df = pd.DataFrame({"c":[random.random() for _ in range(20)]})

    # Manipulating data in Treasure Data via Python.
    # Uses https://github.com/treasure-data/td-client-python

    tdc = tdclient.Client(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])

    try:
        tdc.create_database(database_name)
    except tdclient.errors.AlreadyExistsError:
        pass

    try:
        tdc.create_log_table(database_name, table_name)
    except tdclient.errors.AlreadyExistsError:
        pass

    table_path = f"{database_name}.{table_name}"
    td.to_td(df, table_path, con, if_exists='replace', index=False)
