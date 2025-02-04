import os
import pandas as pd
import pytd

def main(**kwargs):
  tdAPIkey = os.getenv("TD_API_KEY")
  tdAPIendpoint = os.getenv("TD_API_ENDPOINT")
  database = kwargs.get('db')
  in_table = kwargs.get('in_tbl')
  out_table = kwargs.get('out_tbl')
  csv_filename = 'temp.csv'

  td = pytd.Client(apikey=tdAPIkey, 
              endpoint=tdAPIendpoint, 
              database=database, 
              default_engine='presto')

  res = td.query(f'SELECT * FROM {database}.{in_table}')
  df = pd.DataFrame(**res)
  print(df)
  df.to_csv(csv_filename, sep=',', index=False, encoding='utf-8')
  print("Script directory:", os.path.dirname(os.path.abspath(__file__)))
  print("Stored csv directory:", os.path.dirname(os.path.abspath(csv_filename)))
  out_df = pd.read_csv(csv_filename)
  print(df)
  
  td.load_table_from_dataframe(out_df,f'{database}.{out_table}',writer='bulk_import',if_exists='overwrite')

# Main
if __name__ == "__main__":
    main()
