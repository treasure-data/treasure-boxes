import os
import requests
import json
import pandas as pd
import pytd
import re
import python_script.S3 as s3

td_api_key = os.environ['TD_API_KEY']
td_endpoint_base = os.environ['TD_API_SERVER']
td_api_cdp = os.environ['TD_API_CDP']
td_home = os.environ['TD_HOME']

def uploadDataToTD(data, td_write_db, td_write_table):
    try:
        client = pytd.Client(apikey=td_api_key,endpoint=td_endpoint_base,database=td_write_db, default_engine='presto')
    except BaseException:
        raise Exception('Error calling pytd.Client')

    try:
        client.load_table_from_dataframe(data, td_write_table, writer='bulk_import', if_exists='append')
    except BaseException:
        raise Exception('Error writing table back into TD Database')


def getListSegmentsfromTD(td_read_db, td_read_table):
    query = f'''select array_join(array_agg(current_node_id), ',') as segments  
          from (
            select current_node_id
            from {td_read_db}.{td_read_table}
            where current_node_type='segment-batch' 
            group by 1
          )'''
    try:
        client = pytd.Client(apikey=td_api_key,endpoint=td_endpoint_base,database=td_read_db, default_engine='presto')
    except BaseException:
        raise Exception('Error calling pytd.Client')

    try:
        dt = client.query(query)
        df = pd.DataFrame(columns=dt['columns'], data=dt['data'])
        print(df)
        return df['segments'].values[0]
    except BaseException as ex:
        raise Exception('Error reading table from TD Database')
        return ''


def saveDatatoLocal(json_data):
    try:
      
      folder = f'{td_home}/pmi_master_seg'
      os.system(f"rm -rf {folder}")
      os.system(f"mkdir {folder}")
      
      local_file_path = f'{folder}/temp_segment_json.json'

      with open(local_file_path, 'w') as f:
        json.dump(json_data, f)
      return local_file_path
    except Exception as e:
      raise Exception(f"Error saving data to local: {str(e)}")
      return None


def exportSegmentData(url):
        headers = {
            "AUTHORIZATION": f"TD1 {td_api_key}"
            }
      
        try:
            response = requests.get(url, headers=headers)
            data = response.text
            print(data)
            data = json.loads(data)
            formatted_json = json.dumps(data)
            formatted_json = f'{{"_col0":{formatted_json}}}'
            result = json.loads(formatted_json)
            response.raise_for_status()
            if response.ok:
                return result
        except Exception as ex:
            raise Exception(f'Export segment data failed {ex}')
        return None 


def exportSubSegmentData(url,segment_id):
        headers = {
            "AUTHORIZATION": f"TD1 {td_api_key}"
            }
      
        try:
            response = requests.get(f'{url}/{segment_id}', headers=headers)
            data = response.text
            data = json.loads(data)
            response.raise_for_status()
            if response.ok:
                return data
        except Exception as ex:
            raise Exception(f'Export segment data failed {ex}')
        return None 

def writeFolderConfigtoTD(json_data, db_name, table):
    pattern = r"([:\[,{]\s*)'(.*?)'(?=\s*[:,\]}])"
    try:
      df = pd.DataFrame(json_data["_col0"]["data"])
      df = df.applymap(lambda x: re.sub(pattern, r'\1"\2"',str(x)))
      print(df)
      uploadDataToTD(df,db_name,table)
    except Exception as ex:
      raise Exception(f'Write Folder Config data to TD failed {ex}')


def writeMasterSegmenttoTD(json_data, db_name, table):
    pattern = r"([:\[,{]\s*)'(.*?)'(?=\s*[:,\]}])"
    try:
      df = pd.DataFrame()
      df['config'] = [json_data["_col0"]]
      df = df.applymap(lambda x: re.sub(pattern, r'\1"\2"',str(x)))
      print(df)
      uploadDataToTD(df,db_name,table)
    except Exception as ex:
      raise Exception(f'Write Master Segment data to TD failed {ex}')

def writeAllSegmentstoTD(data, db_name, table):
    pattern = r"([:\[,{]\s*)'(.*?)'(?=\s*[:,\]}])"
    try:
      df = pd.DataFrame(data)
      df = df.applymap(lambda x: re.sub(pattern, r'\1"\2"',str(x)))
      print(df)
      uploadDataToTD(df,db_name,table)
    except Exception as ex:
      raise Exception(f'Write all Segments data to TD failed {ex}')


def main(url,s3_object_key,bk_type,db_name, table, s3_table):
  print("********************************CALL TD API***********************************")
  url = f'{td_api_cdp}/{url}'
  data = exportSegmentData(url)
  local_file_path = saveDatatoLocal(data)
  print("********************************WRITE RESULT TO S3***********************************")
  s3.uploadFiletoS3(s3_object_key,local_file_path, db_name, s3_table)
  print("********************************WRITE RESULT TO TD***********************************")
  if bk_type == 'folder_config':
    writeFolderConfigtoTD(data, db_name, table)
  elif bk_type == 'master_segment':
    writeMasterSegmenttoTD(data,db_name,table)

def main_all_segments(url,s3_object_key,db_name, read_table, write_table, s3_table):
  print("********************************CALL TD API***********************************")
  url = f'{td_api_cdp}/{url}'
  segments = getListSegmentsfromTD(db_name, read_table)
  list_segments = list(segments.split(","))
  data = []
  for sg in list_segments:
    js = exportSubSegmentData(url,sg)
    data.append(js)
  data_json = json.dumps(data)
  data_json = f'{{"data":{data_json}}}'
  data_json = json.loads(data_json)
  local_file_path = saveDatatoLocal(data_json)
  print("********************************WRITE RESULT TO TD***********************************")
  writeAllSegmentstoTD(data_json, db_name, write_table)
  print("********************************WRITE RESULT TO S3***********************************")
  s3.uploadFiletoS3(s3_object_key,local_file_path,db_name,s3_table)