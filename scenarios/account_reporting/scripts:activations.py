import os
import pytd
import requests
import pandas as pd
import json

def get_list(destination_db, destination_tbl):
  # get all audiences
  audience_list = get_audience_list()
  print(f'{len(audience_list)} audiences found')

  activations_df = pd.DataFrame()

  # get activations list for each audience
  for audience in audience_list:
    try:
        activations = get_activations_by_audience(audience['id'])
        
        if len(activations) > 0:
            activations_df = activations_df.append(activations,ignore_index=True)
            activations_df['audience'] = audience['name']
    except:
        print('Error retrieving activation details for audience ' + audience['id'])

  # clean activations data 
  activations_df.rename(columns={'id':'activationid'}, inplace=True)
  activations_df['lastsessionid'] = activations_df["executions"].apply(get_last_execution_detail, args = ('workflowSessionId',))
  activations_df['lastsessiondate'] = activations_df["executions"].apply(get_last_execution_detail, args = ('createdAt',))
  activations_df['lastsessionstatus'] = activations_df["executions"].apply(get_last_execution_detail, args = ('status',))
  activations_df['createduser'] = activations_df['createdBy'].apply(get_name_from_user)
  activations_df['updateduser'] = activations_df['updatedBy'].apply(get_name_from_user)
  activations_df.drop(['executions','createdBy','updatedBy'],axis=1,inplace=True)

  if activations_df.empty:
    print('No activations found on account')
  else:
    # write activations to db
    apikey = os.environ["TD_API_KEY"]
    td_api_baseurl = os.environ["TD_API_BASEURL"]
    client = pytd.Client(endpoint=td_api_baseurl,apikey=apikey,database=destination_db,default_engine='presto')
    client.load_table_from_dataframe(activations_df,destination=destination_tbl,writer='bulk_import',if_exists='overwrite')

def get_activations_by_audience(audience_id):
  return cdp_get(f"/audiences/{audience_id}/syndications")

def get_audience_list():
    return cdp_get("/master_segments")

def cdp_get(endpoint):
  apikey = os.environ["TD_API_KEY"]
  headers = {'Authorization': 'TD1 ' + apikey}
  
  cdp_api_baseurl = os.environ["CDP_API_BASEURL"]
  request_url = cdp_api_baseurl + endpoint 

  response = requests.get(url = request_url, headers = headers)
  return response.json()

def get_last_execution_detail(executions, field):
    if len(executions) == 0:
        return ''
    return executions[0][field]

def get_name_from_user(user):
    if len(user) == 0:
        return 'n/a'
    return user['name']