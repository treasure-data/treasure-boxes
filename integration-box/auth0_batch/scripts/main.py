import logging 
import json
import time
import os
import gzip
from io import StringIO

import requests

try:
    import pytd
    import pandas as pd
except:
    import sys
    os.system(f"{sys.executable} -m pip install -U pandas pytd")

logger = logging.getLogger(__name__)
logging.basicConfig()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False

def load(database, table, td_endpoint, auth0_endpoint, auth0_token, connection_id):
    """
    entrypoint for this script.
    Export all user information in Auth0 and load into TD.

    Parameters
    ------
    database : str
        target database name
    table : str
        target table name
    td_endpoint  : str
        TreasureData API endpoint. Includes scheme and trailing slash.
    auth0_endpoint : str
        Auth0 Management API endpoint. Includes scheme and trailing slash.
    auth0_token : str
        access token retreived from /oauth/token
    connection_id : str
        Auth0 Connection id
    """
    jobid = create_export_job(auth0_endpoint, auth0_token, connection_id)
    if not jobid:
        raise Exception("Cannot create export job.")
    df = get_export_result(auth0_endpoint, auth0_token, jobid)
    if df is None:
        raise Exception("Cannot retrieve remote URL during execution. Possibly timeout?")

    load_into_td(df, database, table, td_endpoint)

def create_export_job(endpoint, token, connection_id):
    """
    Issue user export job.

    Parameters
    -----
    endpoint: str
        Auth0 endpoint.
    token : str
        Auth0 access token
    connection_id : str
        Auth0 connection id

    Returns
    ------
    str or None
        return job id for the export job. If failed, this function returns None.
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    payload = {
        "connection_id": connection_id,
        "format": "csv",
        "fields": [
            {"name": "email"},
            {"name": "identities[0].connection", "export_as": "provider"}
        ]
    }
    resp = requests.post(f"{endpoint}api/v2/jobs/users-exports", headers=headers, json=payload)
    logger.debug("%s", resp.text)
    return resp.json().get("id")


def get_export_result(endpoint, token, jobid):
    """
    Download result file from Auth0 and wrap it in pandas.DataFrame.

    Parameters
    -----
    endpoint : str
        Auth0 endpoint
    token : str
        Auth0 access token
    jobid : str
        Job ID

    Returns
    -----
    pandas.DataFrame or None
        DataFrame. If export failed or exceeds MAX_RETRY attempt, returns None.
    """
    MAX_RETRY = 10
    INTERVAL = 10

    headers = {
        'content-type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    location = None
    for i in range(0, MAX_RETRY):
        logger.info("Checking export job status... : %s/%s", i+1, MAX_RETRY)
        resp = requests.get(f"{endpoint}api/v2/jobs/{jobid}", headers=headers)
        logger.debug("%s", resp.text)
        if "location" in resp.json():
            location = resp.json()["location"]
            break
        time.sleep(INTERVAL)

    if not location:
        return None

    resp = requests.get(location)
    return pd.read_csv(StringIO(gzip.decompress(resp.content).decode('utf-8')))

def load_into_td(df, database, table, endpoint):
    """
    Load Dataframe into TD

    Parameters
    ------
    df : pandas.DataFrame
        Dataframe
    database : str
        target database
    table : str
        target table
    endpoint : str
        TD API endpoint.
    """
    apikey = os.getenv('TD_APIKEY')
    tdclient = pytd.Client(database=database, apikey=apikey, endpoint=endpoint)
    tdclient.load_table_from_dataframe(df, f'{database}.{table}', if_exists='overwrite')
    logger.info("Finished writing data for %s", f'{database}.{table}')

if __name__ == '__main__':
    pass