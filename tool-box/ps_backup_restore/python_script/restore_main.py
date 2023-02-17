import json
import digdag
import os
import sys
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import pytd
import pandas as pd
from boto3 import client

# restore folder structure into Audience Studio V5
# get folder configs from s3/td table load into dataframe
# iterate from parent folder to child folders and segments
# create them with CDP API as you iterate
td_api_key = os.environ['TD_API_KEY']
td_endpoint = os.environ['TD_API_SERVER']
database = os.environ['database']
table = os.environ['table']

# NB. Queries built using string formatting due to Presto Python client underlying pyTD not supporting query parameters. Deemed safe in this instance as sole input is YAML config.

# create dataframe for all entities
sqlFile = f'''WITH records AS ( select CAST(json_extract(_col0, \'$.data\') as ARRAY<JSON>) records from {table} ),data_f as (SELECT CAST(json_extract(record, \'$.relationships.parentFolder.data.id\') as int) parent_node_id, CAST(json_extract(record, \'$.relationships.parentFolder.data.type\') as VARCHAR) parent_node_type, CAST(json_extract(record, \'$.id\') AS INT) current_node_id, CAST(json_extract(record, \'$.type\') AS VARCHAR) current_node_type, CAST(json_extract(record, \'$.attributes.name\') AS VARCHAR) current_node_name, CAST(json_extract(record, \'$.attributes.description\') AS VARCHAR) current_node_desc FROM records CROSS JOIN UNNEST(records) AS t(record) ) select * from data_f where current_node_type!=\'folder-segment\' order by current_node_id'''

#create dataframe for folder struct
sqlFileFolder = f'''WITH records AS ( select CAST(json_extract(_col0, \'$.data\') as ARRAY<JSON>) records from {table} ),data_f as (SELECT CAST(json_extract(record, \'$.relationships.parentFolder.data.id\') as int) parent_node_id, CAST(json_extract(record, \'$.relationships.parentFolder.data.type\') as VARCHAR) parent_node_type, CAST(json_extract(record, \'$.id\') AS INT) current_node_id, CAST(json_extract(record, \'$.type\') AS VARCHAR) current_node_type, CAST(json_extract(record, \'$.attributes.name\') AS VARCHAR) current_node_name, CAST(json_extract(record, \'$.attributes.description\') AS VARCHAR) current_node_desc FROM records CROSS JOIN UNNEST(records) AS t(record) ) select * from data_f where current_node_type=\'folder-segment\' order by parent_node_id asc, current_node_id'''

client_td = pytd.Client(apikey=td_api_key, endpoint=td_endpoint, database=database)
results = client_td.query(sqlFile)
df = pd.DataFrame(**results)

df['parent_node_id'] = df['parent_node_id'].fillna(0)
df['parent_node_id'] = df['parent_node_id'].astype(int)

results_f = client_td.query(sqlFileFolder)
df_fol = pd.DataFrame(**results_f)

df_fol['parent_node_id'] = df_fol['parent_node_id'].fillna(0)
df_fol['parent_node_id'] = df_fol['parent_node_id'].astype(int)
p = df_fol.loc[df_fol['parent_node_id'] == 0, 'current_node_id']


BUCKET = os.environ['AWS_BUCKET']
FOLDER_FILE_TO_READ = os.environ['AWS_PATH_PREFIX']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
root_id = os.environ['ROOT_FOLDER_ID']

client = client('s3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                )
# res_seg = client.get_object(Bucket=BUCKET, Key=SEG_FILE_TO_READ)
# segments = res_seg["Body"]
# segments = json.load(segments)
# segments = json.loads(segments['_col0'])

res_fol = client.get_object(Bucket=BUCKET,Key=FOLDER_FILE_TO_READ)
folders = res_fol["Body"]
folders = json.load(folders)
folders = json.loads(folders['_col0'])

folder_dict = {}
segment_dict = {}

headers = {"Authorization": "TD1 "+td_api_key,
"Content-Type": "application/json"}
#auth = HTTPBasicAuth('Authorization', "TD1 " + td_api_key)

def create_folder(p_id, c_id):
    for f in folders['data']:
        if int(f['id']) == c_id:
            f['relationships']['parentFolder']['data']['id'] = str(p_id)
            r = requests.post("https://api-cdp.treasuredata.com/entities/folders",headers=headers,data=json.dumps(f))
            resp = r.json()
            if "data" in resp:
                return resp["data"]["id"]
            
    return

def create_folder_struct(p_id, c_id):
    folder_df = df_fol.loc[df_fol['parent_node_id'] == c_id, ['current_node_id','current_node_name','current_node_type','current_node_desc']]
    if folder_df.empty:
        return
    for row in folder_df.itertuples():
        for f in folders['data']:
            if row.current_node_id == int(f['id']):
                f['relationships']['parentFolder']['data']['id'] = str(p_id)
                r = requests.post("https://api-cdp.treasuredata.com/entities/folders",headers=headers,data=json.dumps(f))
                resp = r.json()
                if "data" in resp:
                    folder_dict[row.current_node_id] = resp["data"]["id"]
                    create_folder_struct(int(resp["data"]["id"]),row.current_node_id)
    print(folder_dict)

def create_entity(c_id):
    p_id = "null"

    #check if segment is already created and return the new entity id
    if int(c_id) in segment_dict:
        return segment_dict[int(c_id)]
    
    #get parent id of this segment
    df_2 = df.loc[df['current_node_id'] == c_id, ['parent_node_id','current_node_id','current_node_name','current_node_type','current_node_desc']]
    print(df_2.head())
    if df_2.empty:
        print("Empty dataframe")
        return
    else:
        p_id = str(folder_dict[int(df_2['parent_node_id'].values[0])])
        print("p_id ", p_id)

    for f in folders['data']:
        if int(df_2['current_node_id'].values[0]) == int(f['id']):
            if df_2['current_node_type'].values[0] == 'predictive-segment':
                print(f["attributes"]["segmentId"])
                s_id = create_entity(int(f["attributes"]["segmentId"]))
                f['attributes']['segmentId'] = str(s_id)
                f['relationships']['parentFolder']['data']['id'] = str(p_id)
                r = requests.post("https://api-cdp.treasuredata.com/entities/predictive_segments",headers=headers,data=json.dumps(f))
                resp = r.json()
                if "data" in resp:
                    segment_dict[int(df_2['current_node_id'].values[0])] = resp["data"]["id"]
                    return str(resp["data"]["id"])
            elif df_2['current_node_type'].values[0] == 'segment-batch':
                for condition in f['attributes']['rule']['conditions'][0]['conditions']:
                    if "type" in condition:
                        if condition['type'] == "Reference" or condition['type'] == "PredictiveScoreReference":
                            ref_id = create_entity(int(condition['id']))
                            condition['id'] = str(ref_id)
                f['relationships']['parentFolder']['data']['id'] = str(p_id)
                r = requests.post("https://api-cdp.treasuredata.com/entities/segments",headers=headers,data=json.dumps(f))
                resp = r.json()
                if "data" in resp:
                    segment_dict[int(df_2['current_node_id'].values[0])] = resp["data"]["id"]
                    return str(resp["data"]["id"])

def main():
  folder_dict[p.values[0]] = str(root_id)
  create_folder_struct(int(root_id),p.values[0])
  #create_entity(113531)
  for ind in range(len(df)):
       create_entity(df.loc[ind, ["current_node_id"]].values[0])