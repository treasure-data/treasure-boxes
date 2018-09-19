# CSV File Import
# Bulk Import by td-client-python

import sys
import os

print('Installing libs ...')
os.system("pip install --upgrade pip")
os.system("pip install td-client")
os.system("pip install pandas-td")

# Params
print('Setting params ...')
endpoint='https://api.treasuredata.com/'
td_apikey = os.environ.get('td_apikey')
filename = 'sample.csv'
dbname = 'dbname'
tablename = 'tablename'

def generate_sample_df():
  import pandas as pd
  d = {
        'col1': [1, 2, 3, 4, 5],
        'col2': ['a','b','c','d','e'],
        'time': [11, 22, 33, 44, 55]}
  df = pd.DataFrame(data=d)
  return df

def add_time_col(df):
  if not 'time' in df:
    from datetime import datetime
    print('Adding a time column ...')
    df['time'] = int(datetime.now().strftime('%s'))
  print(df)

def output_csv(df):
  # Store data frame to local
  print('Storing data frame to local ...')
  df.to_csv(filename, index=False)

def bulk_import_to_td():
  # time column is needed
  import sys
  import tdclient
  import time
  import warnings

  with tdclient.Client(td_apikey) as td:
    session_name = "session-%d" % (int(time.time()),)
    bulk_import = td.create_bulk_import(session_name, dbname, tablename)
    try:
      #for file_name in "to_csv_out.csv":
      part_name = "part-%s" % (filename,)
      bulk_import.upload_file(part_name, "csv", filename)
      bulk_import.freeze()
    except:
      bulk_import.delete()
      raise
    bulk_import.perform(wait=True)
    if 0 < bulk_import.error_records:
        warnings.warn("detected %d error records." % (bulk_import.error_records,))
    if 0 < bulk_import.valid_records:
      print("imported %d records." % (bulk_import.valid_records,))
    else:
      raise(RuntimeError("no records have been imported: %s" % (repr(bulk_import.name),)))
    bulk_import.commit(wait=True)
    bulk_import.delete()

def main():
  df = generate_sample_df()
  add_time_col(df)
  output_csv(df)
  bulk_import_to_td()
