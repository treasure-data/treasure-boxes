import os
import sys
import pandas as pd
import json

os.system(f"{sys.executable} -m pip install --user pytd==1.0.0")
import pytd

def main(url, database, table, column_setting_file):
  #df = pd.read_csv(url)

  column_setting  = json.load(open("csv_setting.json", "r"))
  print(column_setting)
  #header_mapping  = map(lambda v: (v['from_name'], v['to_name']), column_setting.csv_column_setting)
  #df_en           = df.rename(columns = dict(header_mapping))

  #ignore_columns  = map(lambda v: v['en'], filter(lambda x: x['ignore'], column_setting.csv_column_setting))
  #droped_df       = df_en.drop(columns = list(ignore_columns))

  #client = pytd.Client(apikey = os.getenv('apikey'), database = database)
  #client.load_table_from_dataframe(droped_df, table), writer = 'bulk_import', if_exists = 'append')
