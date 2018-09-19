# DataFrame Import
# Streasm Import by pandas-td

import os

# Install Libs
print('Installing Libs ...')
os.system("pip install --upgrade pip")
os.system("pip install pandas-td")

# Set Params
print('Setting Params ...')
endpoint='https://api.treasuredata.com'
td_apikey = os.environ.get('td_apikey')
dbname = 'dbname'
table = 'tablename'
db_table = dbname + '.' + table

def generate_sample_df():
  import pandas as pd
  d = {'col1': [1, 2, 3, 4, 5], 'col2': ['a','b','c','d','e']}
  df = pd.DataFrame(data=d)
  return df

def add_time_col(df):
  if not 'time' in df:
    from datetime import datetime
    print('Adding a time column ...')
    df['time'] = int(datetime.now().strftime('%s'))
  print(df)

def stream_import_to_td(df):
  import pandas_td as td

  # Connect TD
  con = td.connect(td_apikey, endpoint)
  engine = con.query_engine(database=dbname, type='presto')

  # Stream Import to TD
  print('Stream Importing ...')
  td.to_td(df, db_table, con, if_exists='replace', index=False, time_col='time')

def main():
  df = generate_sample_df()
  add_time_col(df)
  stream_import_to_td(df)
