import os

import pytd
import requests
import pandas as pd

print(pytd.version.__version__)

td_endpoint = os.environ["td_endpoint"]
td_api_key = os.environ["apikey"]
td_database = os.environ["td_database"]
td_table = os.environ["td_table"]
cdp_url = os.environ["cdp_url"]
cdp_auth_key = "TD1 " + td_api_key


def uploadDataToTD(td_endpoint, td_api_key, dataframe, td_database, td_table):
    client = pytd.Client(
        apikey=td_api_key,
        endpoint=td_endpoint,
        database=td_database,
        default_engine="hive",
    )
    client.load_table_from_dataframe(
        dataframe, td_table, writer="bulk_import", if_exists="append", ignore_index=True
    )


def getSegmentLists():

    header_payload = {"authorization": cdp_auth_key}
    getresponse = requests.get(cdp_url, headers=header_payload)
    api_res = getresponse.json()
    jlen = len(api_res)
    print(api_res)
    print(jlen)
    if jlen == 0:
        print("Finish: No contents to import")
    else:
        td_dataframe = pd.DataFrame()
        td_dataframe = td_dataframe.append(api_res)
        df_to_upload_td = td_dataframe
        print(df_to_upload_td)
        uploadDataToTD(td_endpoint, td_api_key, df_to_upload_td, td_database, td_table)
