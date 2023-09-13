import os
import sys
import pandas as pd 
import requests
import pytd

def process(destination_db, destination_tbl):
  iterable_apikey = os.environ["ITERABLE_API_KEY"]
  api_url = 'https://api.iterable.com/api/campaigns'

  headers = {"Api-Key":iterable_apikey}
  response = requests.get(api_url,headers=headers)
  response_df = pd.DataFrame(response.json()['campaigns'])
  
  ready_campaigns = response_df.query("campaignState == 'Ready'")
  
  td_apikey = os.environ["TD_API_KEY"]
  client = pytd.Client(apikey=td_apikey,database=destination_db)
  client.load_table_from_dataframe(ready_campaigns, destination_tbl, if_exists='overwrite')