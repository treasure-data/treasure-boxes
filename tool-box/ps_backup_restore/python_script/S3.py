import boto3
import json
import os
import pandas as pd
import pytd
from boto3.s3.transfer import TransferConfig


BUCKET = os.environ['AWS_BUCKET']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
td_api_key = os.environ['TD_API_KEY']
td_endpoint_base = os.environ['TD_API_SERVER']

def uploadFiletoS3(s3_object_key,local_file_path, db_name, table_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    config = boto3.s3.transfer.TransferConfig(multipart_chunksize=1024 * 1) #1MB

    try:
        s3.upload_file(local_file_path, BUCKET, s3_object_key, Config=config)
        storeS3ObjectKeytoTD(s3_object_key, db_name, table_name)
    except Exception as e:
        raise Exception(f"Error writing the backup data to S3: {str(e)}")

def storeS3ObjectKeytoTD(s3_object_key, db_name, table_name):
  df = pd.DataFrame()
  df['bucket'] = [BUCKET]
  df['s3_object_key'] = [s3_object_key]
  print(df)

  try:
    client = pytd.Client(apikey=td_api_key,endpoint=td_endpoint_base,database=db_name, default_engine='presto')
  except BaseException:
      raise Exception('Error calling pytd.Client')

  try:
    client.load_table_from_dataframe(df, table_name, writer='bulk_import', if_exists='append')
  except BaseException:
    raise Exception('Error writing table back into TD Database')
  