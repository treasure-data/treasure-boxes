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


def upload(**kwargs):
    acid = kwargs.get('acid') 
    api_key = kwargs.get('api_key')
    service_id = kwargs.get('service_id')

    endpoint = 'https://line-api.dialogone.jp/v1/line/external-segments/file'
    url = f"{endpoint}/{service_id}/{acid}"

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
        token = hashlib.sha256(f"{api_key}{file_name}".encode("utf-8")).hexdigest()
        headers = {
            "X-DialogOne-Access-Token": token
        }

        files = {
            'file': (file_name, csv, "text/csv")
        }
        
        res = requests.post(
            url,
            headers=headers,
            files=files 
        )

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
    csvs = []
    row_len_limit = 50000000 # max data length per a API call

    client = pytd.Client(apikey=os.getenv("TD_API_KEY"), database=database)
    query = f"""
        SELECT
            {column}
        FROM 
            {table}
        WHERE 
            {column} is not null
            AND REGEXP_LIKE({column}, 'U[0-9a-f]{{{32}}}')
        """

    res = client.query(query)
    df = pd.DataFrame(**res)  

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
