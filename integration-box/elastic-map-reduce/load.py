#!/usr/bin/python

import pandas_td as td

print("load.py started")

con = td.connect(apikey="TD_APIKEY", endpoint="https://api.treasuredata.com")

# Type: Presto, Database: sample_datasets
engine = td.create_engine("presto:sample_datasets", con=con)

# Read Treasure Data query from into a DataFrame.
df = td.read_td_query(
    """
SELECT time, close FROM nasdaq LIMIT 100
""",
    engine,
    index_col="time",
    parse_dates={"time": "s"},
)

print(df.head)

# Output DataFrame to TreasureData via Streaming Import. (If your dataset is large, this method is not recommended.)
td.to_td(df, "workflow_temp.test_emr", con, if_exists="replace", index=False)

print("load.py finished")
