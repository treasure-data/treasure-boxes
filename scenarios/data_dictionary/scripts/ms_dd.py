#scripts/ms_dd.py
import os
import pandas as pd
import pytd
import requests

def main(**kwargs):
  # passed params
  td_api_key = os.getenv('TD_API_KEY')
  # params from config.yml
  td_api_ep = kwargs.get('td_api_ep')
  ms_config_ep = kwargs.get('ms_config_ep')
  ms_id = kwargs.get('ms_id')
  temp_db = kwargs.get('temp_db')
  temp_schema_tbl = kwargs.get('temp_schema_tbl')
  temp_ms_conf_tbl = kwargs.get('temp_ms_conf_tbl')
  # Init import from / export to TD table
  td = pytd.Client(apikey = td_api_key, 
                  endpoint = td_api_ep, 
                  database = temp_db, 
                  default_engine = 'presto')

  # Fetch master segment config
  url = ms_config_ep + str(ms_id)
  headers = {'Authorization': f'TD1 {td_api_key}'}
  res = requests.get(url, headers = headers)
  ms_conf = res.json()

  # Extract and store master segment's name
  ms_name = ms_conf.get('name', 'N/A')
  ms_conf_df = pd.DataFrame({'name': [ms_name]})
  td.load_table_from_dataframe(ms_conf_df, f'{temp_db}.{temp_ms_conf_tbl}', writer='bulk_import', if_exists='overwrite')

  # Extract master table database and table
  master_db = ms_conf.get('master', {}).get('parentDatabaseName', None)
  master_tbl = ms_conf.get('master', {}).get('parentTableName', None)
  # Fetch master table schema
  # Describe schema: Column, Type, Extra, Comment
  master_res = td.query(f'DESCRIBE {master_db}.{master_tbl}')
  master_df = pd.DataFrame(**master_res)
  master_df = master_df.drop('Extra', axis=1)
  master_df['database'] = master_db
  master_df['table'] = master_tbl
  master_df['column_alias'] = ''
  # Send data to TD table
  td.load_table_from_dataframe(master_df, f'{temp_db}.{temp_schema_tbl}', writer='bulk_import', if_exists='overwrite')

  # Extract database, table, and columns for attribute tables
  # Unique db, tbl set
  attribute_tbls = {
    (attr_tbl['parentDatabaseName'], attr_tbl['parentTableName'])
    for attr_tbl in ms_conf.get('attributes', [])
  }
  # All db, table, column alias, column name list
  attribute_tbls_cols = [
    (attr['parentDatabaseName'], attr['parentTableName'], attr['name'], attr['parentColumn'])
    for attr in ms_conf.get('attributes', [])
  ]
  # Build attribute table schema
  for attr_tbls_db, attr_tbls_tbl in attribute_tbls:   
    attr_res = td.query(f'DESCRIBE {attr_tbls_db}.{attr_tbls_tbl}')
    attr_df = pd.DataFrame(**attr_res)
    attr_dict_list = []
    for attr_db, attr_tbl, col_alias, col_name in attribute_tbls_cols:
      if attr_db == attr_tbls_db and attr_tbl == attr_tbls_tbl:
        attr_dict = {
            'database': attr_db,
            'table': attr_tbl,
            'column_alias': col_alias,
            'column': col_name,
            'type': attr_df[attr_df['Column'] == col_name].iloc[0,1],
            'comment': attr_df[attr_df['Column'] == col_name].iloc[0,3],
        }
        attr_dict_list.append(attr_dict)
    attr_df = pd.DataFrame(attr_dict_list)
    # Send data to TD table
    td.load_table_from_dataframe(attr_df, f'{temp_db}.{temp_schema_tbl}', writer='bulk_import', if_exists='append')

  # Extract database, table, and columns for behavior tables
  # Unique db, tbl set
  behavior_tbls = {
    (behav_tbl['parentDatabaseName'], behav_tbl['parentTableName'])
    for behav_tbl in ms_conf.get('behaviors', [])
  }
  # All db, table, column alias, column name list
  behavior_tbls_cols = []
  for behav in ms_conf.get('behaviors', []):
    behav_db = behav['parentDatabaseName']
    behav_tbl = behav['parentTableName']
    if behav.get('allColumns', True):
      behav_res = td.query(f'DESCRIBE {behav_db}.{behav_tbl}')
      behav_df = pd.DataFrame(**behav_res)
      for row in behav_df.iterrows():
        behavior_tbls_cols.append([behav_db, behav_tbl, '', row[1]['Column']])
    else:
      behav_schema = [
              (behav_db, behav_tbl, schema['name'], schema['parentColumn'])
              for schema in behav.get('schema', [])
          ]
      behavior_tbls_cols.extend(behav_schema)
  # Build behavior table schema
  for behav_tbls_db, behav_tbls_tbl in behavior_tbls:   
    behav_res = td.query(f'DESCRIBE {behav_tbls_db}.{behav_tbls_tbl}')
    behav_df = pd.DataFrame(**behav_res)
    behav_dict_list = []
    for behav_db, behav_tbl, col_alias, col_name in behavior_tbls_cols:
      if behav_db == behav_tbls_db and behav_tbl == behav_tbls_tbl:
        behav_dict = {
            'database': behav_db,
            'table': behav_tbl,
            'column_alias': col_alias,
            'column': col_name,
            'type': behav_df[behav_df['Column'] == col_name].iloc[0,1],
            'comment': behav_df[behav_df['Column'] == col_name].iloc[0,3],
        }
        behav_dict_list.append(behav_dict)
    behav_df = pd.DataFrame(behav_dict_list)
    # Send data to TD table
    td.load_table_from_dataframe(behav_df, f'{temp_db}.{temp_schema_tbl}', writer='bulk_import', if_exists='append')

# Main
if __name__ == "__main__":
    main()
