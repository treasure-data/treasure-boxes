import os
import pytd
import requests
import pandas as pd
import json

def get_list(destination_db, destination_tbl):
  # get all queries
  queries_list = get_queries_list()
  print(f'{len(queries_list)} queries found')

  # remove sql from result 
  queries_df = pd.DataFrame(queries_list)
  queries_df.drop(['query'],axis=1,inplace=True)

  if queries_df.empty:
    print('No queries found on account')
  else:
    # write queries to db
    apikey = os.environ["TD_API_KEY"]
    td_api_baseurl = os.environ["TD_API_BASEURL"]
    client = pytd.Client(endpoint=td_api_baseurl,apikey=apikey,database=destination_db,default_engine='presto')
    client.load_table_from_dataframe(queries_df,destination=destination_tbl,writer='bulk_import',if_exists='overwrite')

def get_queries_list():
    return td_get("/v3/schedule/list")

def td_get(endpoint):
  apikey = os.environ["TD_API_KEY"]
  headers = {'Authorization': 'TD1 ' + apikey}
  
  td_api_baseurl = os.environ["TD_API_BASEURL"]
  request_url = td_api_baseurl + endpoint 

  response = requests.get(url = request_url, headers = headers)
  return (response.json())['schedules']