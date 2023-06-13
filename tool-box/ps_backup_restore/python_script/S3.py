import boto3
import json
import os
from boto3.s3.transfer import TransferConfig


BUCKET = os.environ['AWS_BUCKET']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

def uploadFiletoS3(s3_object_key,local_file_path):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    config = boto3.s3.transfer.TransferConfig(multipart_chunksize=1024 * 1) #1MB

    try:
        s3.upload_file(local_file_path, BUCKET, s3_object_key, Config=config)
        print(f"Wrote {s3_object_key} to S3 successfully!")
    except Exception as e:
        raise Exception(f"Error writing the backup data to S3: {str(e)}")

