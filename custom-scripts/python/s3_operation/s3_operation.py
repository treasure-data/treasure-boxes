import os

# Install Libs
print('Installing libs ...')
os.system("pip install --upgrade pip")
os.system("pip install boto3")

# Set Params
print('Setting params ...')
access_key = os.environ.get('s3_access_key')
secret_key = os.environ.get('s3_secret_key')
region = 'us-east-1'
bucketname = 'bucket'
filename = 'file.csv'
new_filename = 'new_file.csv'

def connect_s3():
  import boto3
  print('Connecting S3 ...')
  session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
  s3 = session.resource('s3')
  return s3

def download_s3_file(s3):
  print('Downloading file from S3 ...')
  bucket = s3.Bucket(bucketname)
  bucket.download_file(filename, filename)

def upload_s3_file(s3):
  print('Uploading file to S3 ...')
  bucket = s3.Bucket(bucketname)
  bucket.upload_file(filename, new_filename)

def main():
  s3 = connect_s3()
  download_s3_file(s3)
  upload_s3_file(s3)
