import os
import sys
import pandas as pd
from importlib import import_module

os.system(f"{sys.executable} -m pip install --user pytd==1.0.0")
import pytd

def main():
  url     = os.getenv('url')
  df      = pd.read_csv(url)

  column_setting  = import_module(os.getenv('column_setting'))
  header_mapping  = map(lambda v: (v['from_name'], v['to_name']), column_setting.csv_column_setting)
  df_en           = df.rename(columns = dict(header_mapping))

  ignore_columns  = map(lambda v: v['en'], filter(lambda x: x['ignore'], column_setting.csv_column_setting))
  droped_df       = df_en.drop(columns = list(ignore_columns))

  client = pytd.Client(apikey = os.getenv('apikey'), database = os.getenv('database'))
  client.load_table_from_dataframe(df_en, os.getenv('table'), writer = 'bulk_import', if_exists = 'append')
