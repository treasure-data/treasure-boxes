import os
import sys
os.system(f"{sys.executable} -m pip install -U pytd==1.4.0 td-client")

import pandas as pd
import pytd
import requests
from logging import INFO, StreamHandler, getLogger
import gzip
import hashlib

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


def main(**kwargs):
    database = kwargs.get('database')
    table = kwargs.get('table')
    column = kwargs.get('user_id_column')
    filename = kwargs.get('filename')

    if (len(filename) > 255):
        logger.error(
          f"Filename must be less than 255 characters."
        )
        sys.exit(os.EX_DATAERR)

    # get user list from Treasure Data in CSV format 
    csvs = retrive_user_id_csv(database, table, column)
    
    for i, csv in enumerate(csvs):
        idx = i + 1
        file_name = filename
        if (len(csvs) > 1):
            file_name = f"{filename}_{idx}"
        file_name = f"{file_name}.csv" 

        # post request to Done API 
        res = upload_to_api(file_name, csv)

        if res.status_code != 200:
            logger.error(
                f"Failed to call Done API with http status code {res.status_code}"
            )
            logger.error(res.text)
            sys.exit(os.EX_DATAERR)
        else:
            logger.info(
                f"Succeeded calling Done API with http status code {res.status_code}"
            )

        if csvs[idx:idx + 1]:
            logger.debug('*** Waiting 60 seconds till next call ***')
            time.sleep(60)

def retrive_user_id_csv(database, table, column):
    td_endpoint = os.getenv("TD_ENDPOINT")
    if td_endpoint is None:
        td_endpoint = 'api.treasuredata.com'

    client = pytd.Client(apikey=os.getenv("TD_API_KEY"), database=database)
    sql = get_sql(database, table, column)

    res = client.query(sql)
    df = pd.DataFrame(**res)  

    return divide_data(df)

def get_sql(database, table, column):
    return f"""
        SELECT
            {column}
        FROM 
            {table}
        WHERE 
            {column} is not null
            AND REGEXP_LIKE({column}, 'U[0-9a-f]{{{32}}}')
        """

def divide_data(df):
    # divide data per proper size
    csvs = []
    row_len_limit = 50000000 # max data length per a API call

    while (len(df) > row_len_limit):
        d = df[:row_len_limit]
        r = df[row_len_limit:]
        csv = d.to_csv(header=False, index=False)
        
        logger.info("---- user list as first 10 lines----")
        logger.info("\n".join(csv.splitlines()[:10]))
        logger.info("---- Total number of IDs = " +
                str(len(csv.splitlines())) + "----")

        csvs.append(csv)
        df = r

    if (len(df) > 0):
        csv = df.to_csv(header=False, index=False)
        csvs.append(csv)

    return csvs

def upload_to_api(file_name, csv):
    api_key = os.getenv('DONE_API_KEY')
    url = get_request_url()

    token = hashlib.sha256(f"{api_key}{file_name}".encode("utf-8")).hexdigest()
    headers = {
        "X-DialogOne-Access-Token": token
    }
    files = {
        "file": (file_name, csv, "text/csv")
    }
        
    return requests.post(url,headers=headers,files=files)
    
def get_request_url():
    #endpoint = 'https://line-api.dialogone.jp/v1/line/external-segments/file'
    endpoint = "https://staging-line-api.dialogone.jp/v1/line/external-segments/file"

    acid = os.getenv("DONE_ACID")
    service_id = os.getenv("DONE_SERVICE_ID")

    return f"{endpoint}/{service_id}/{acid}"
