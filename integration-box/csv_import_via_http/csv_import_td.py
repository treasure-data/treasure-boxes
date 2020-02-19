import os
import sys
import pandas as pd
import json

os.system(f"{sys.executable} -m pip install --user pytd==1.0.0")
import pytd

def main(url, database, table, csv_setting_file):
  df = pd.read_csv(url)

  column_setting = json.load(open(csv_setting_file, "r"))
  header_mapping = map(lambda x: (x["from_name"], x["to_name"]), column_setting)
  df_en          = df.rename(columns = dict(header_mapping))

  ignore_columns  = [e["to_name"] for e in column_setting if e["ignore"]]
  droped_df       = df_en.drop(columns = ignore_columns)

  client = pytd.Client(apikey = os.getenv('apikey'), database = database)
  client.load_table_from_dataframe(droped_df, table, writer = 'bulk_import', if_exists = 'append')
