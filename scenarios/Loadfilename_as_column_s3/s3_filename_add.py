import os
import io

AWS_ACCESS_KEY=os.environ.get('s3_access_key')
AWS_SECRET_ACCESS_KEY=os.environ.get('s3_secret_key')
BUCKET_NAME=os.environ.get('s3_bucket')
PATH_PREFIX=os.environ.get('path_prefix')
UPLOAD_PATH_PREFIX=os.environ.get('upload_path_prefix')
DATAFILE=os.environ.get('datafile')


def set_s3_config(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    homepath=os.environ.get("HOME");
    configDir=homepath + "/.aws"
    configFile="credentials"
    credential="[default]\n" + "aws_access_key_id=" + AWS_ACCESS_KEY + "\n" + "aws_secret_access_key=" + AWS_SECRET_ACCESS_KEY + "\n"
    print("creating directries " + configDir + " if not exist")
    os.makedirs(configDir, exist_ok=True)
    file=open(configDir + "/" + configFile, "w")
    file.write(credential)
    file.close()


def get_all_keys(bucket: str=BUCKET_NAME, prefix: str=PATH_PREFIX, keys: []=[], marker: str='') -> [str]:
    from boto3 import Session
    s3client = Session().client('s3')
    """
    See: https://qiita.com/ikai/items/38c52e0c459792a4da46
    """
    response = s3client.list_objects(Bucket=bucket, Prefix=prefix, Marker=marker)
    if 'Contents' in response:
        keys.extend([content['Key'] for content in response['Contents']])
        if 'IsTruncated' in response:
            return get_all_keys(bucket=bucket, prefix=prefix, keys=keys, marker=keys[-1])
    return keys
    #print(keys)

def read_files(keys):
    import boto3
    s3=boto3.resource('s3')
    if os.path.isfile(DATAFILE):
        os.remove(DATAFILE)
    f = open(DATAFILE, 'a')
    for key in keys:
        response=s3.Object(BUCKET_NAME,key).get()
        body=response['Body'].read()
        #return io.StringIO(line.decode('utf-8'))
        #print(body.decode('utf-8'))
        f.write(key.replace(PATH_PREFIX + '/', '', 1) + ',' + body.decode('utf-8'))
    f.close()
    bucket=s3.Bucket(BUCKET_NAME)
    bucket.upload_file(DATAFILE, UPLOAD_PATH_PREFIX + '/' + DATAFILE)


def main_proc():
    os.system("pip install boto3")
    #os.system("date")
    #os.system("pwd")
    #os.system("uname -a")
    #os.system("df -h")
    set_s3_config(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
    read_files(get_all_keys())
    os.system('cat data.tmp')
