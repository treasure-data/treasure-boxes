import os
import io

BUCKET_NAME='td_test_bucket'
PATH_PREFIX='files/'
UPLOAD_PATH_PREFIX='with_filename/'
DATAFILE='data.tmp'

GCP_JSON_KEY=os.environ.get('gcp_json_key')
HOMEPATH=os.environ.get("HOME")
CONFIGDIR=HOMEPATH + "/"
CONFIGFILE="credential.json"

def set_gcp_credential():
    file=open(CONFIGDIR + CONFIGFILE, "w")
    file.write(GCP_JSON_KEY)
    file.close()
    print("created credential.json")


def get_all_keys(bucket: str=BUCKET_NAME, prefix: str=PATH_PREFIX, keys: []=[], marker: str='') -> [str]:
    from google.cloud import storage
    
    storage_client = storage.Client.from_service_account_json(CONFIGDIR + CONFIGFILE)
    #storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    response = storage_client.list_blobs(
        bucket, prefix=prefix, delimiter=''
    )

    for blob in response:
        print(blob.name)
        if blob.name != PATH_PREFIX:
            keys.append(blob.name)
            print(keys)
    return keys

def read_files(keys):
    from google.cloud import storage
    storage_client = storage.Client.from_service_account_json(CONFIGDIR + CONFIGFILE)

    if os.path.isfile(DATAFILE):
        os.remove(DATAFILE)
    f = open(DATAFILE, 'a')
    for key in keys:
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(key)
        body = blob.download_as_string()
        f.write(key.replace(PATH_PREFIX, '', 1) + ',' + body.decode('utf-8'))
    f.close()

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(UPLOAD_PATH_PREFIX + DATAFILE)
    blob.upload_from_filename(DATAFILE)

 
def main_proc():
    os.system("pip install google-cloud-storage")
    set_gcp_credential()
    read_files(get_all_keys())
    os.system('cat data.tmp')