import os
import sys
os.system(f"{sys.executable} -m pip install -U pytd==1.4.0 td-client")
os.system(f"{sys.executable} -m pip install -U google-auth==1.34.0")

from google.auth import jwt
from google.auth import crypt
import pandas as pd
import pytd
import requests
from logging import INFO, StreamHandler, getLogger
import gzip
import time


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

expiry_length = 3600
interval_length = 1

def upload_user_list(database, table, user_id_column, filename, sa_email, acid):
    """Upload a user list for creating Done segments."""

    csvs = []
    row_len_limit = 50000000 # max data length per a API call
    file_name_limit = 255
    endpoint = 'https://line-api.dialogone.jp/v1/line/external-segments/file'

    apikey = os.getenv("TD_API_KEY")
    td_endpoint = os.getenv("TD_ENDPOINT")
    if td_endpoint is None:
        td_endpoint = 'api.treasuredata.com'

    sql = retrive_user_id_sql(table, user_id_column)
    logger.info("---- sql ----")
    logger.info(f"\n{sql}\n")
    logger.info("-------------")    
       
    client = pytd.Client(apikey=apikey, endpoint=td_endpoint, database=database)
    res = client.query(sql)   
    df = pd.DataFrame(**res)  
    
    while (len(df) > row_len_limit):
        d = df[:row_len_limit]
        r = df[row_len_limit:]
        csv = d.to_csv(header=False, index=False)
        csvs.append(csv)
        df = r

    if (len(df) > 0):
        csv = df.to_csv(header=False, index=False)
        csvs.append(csv)

    for i, csv in enumerate(csvs):

        logger.info("---- user list as first 10 lines----")
        logger.info("\n".join(csv.splitlines()[:10]))
        logger.info("---- Total number of IDs = " + str(len(csv.splitlines())) + "----")

        idx = i + 1
        file_name = filename
        if (len(csvs) > 1):
            file_name = "{}_{}".format(filename, idx)

        if (len(file_name) > file_name_limit):
            logger.error(
                f"Filename must be less than 255 characters."
            )
            sys.exit(os.EX_DATAERR)            

        # generate a signed JWT
        token = generate_jwt(sa_email)

        # post request to Done API
        files = {
            'acid': (None, acid),
            'file': (f"{file_name}.csv", csv, 'text/csv')
        }
        headers = {"Authorization": "Bearer {}".format(token.decode())}

        res = requests.post(
            endpoint,
            files=files,
            headers=headers,
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
            logger.debug('*** Waiting till next call ***')
            time.sleep(interval_length)

def retrive_user_id_sql(table, column):
    return f"""
    SELECT
      {column}
    FROM 
      {table}
    WHERE 
      {column} is not null
      AND REGEXP_LIKE({column}, 'U[0-9a-f]{{{32}}}')
    """

def generate_jwt(sa_email):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        "exp": now + expiry_length,
        'iss': sa_email,
        'aud':  sa_email,
        'sub': sa_email,
        'email': sa_email
    }

    # sign with private key
    signer = crypt.RSASigner.from_string(os.getenv("PRIVATE_KEY").replace('\\n', '\n'), os.getenv("PRIVATE_KEY_ID"))
    token = jwt.encode(signer, payload)

    return token
