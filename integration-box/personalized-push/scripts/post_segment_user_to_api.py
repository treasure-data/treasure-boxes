import os
import sys
import time
import requests
import traceback

import pandas as pd
import pytd

from logging import DEBUG, StreamHandler, getLogger

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def fetch_user_data(sql, td_db, td_engine):
    # execute sql and return Job object as a result
    logger.debug(f'===\n{sql}\n===')

    client = pytd.Client(
        apikey=os.environ["TD_API_KEY"],
        endpoint=os.environ["TD_ENDPOINT"],
        database=td_db,
        default_engine=td_engine
    )
    return client.query(sql)


def csv_out(td_job):
    # convert Job object to CSV data
    # divide data if it exceed the limit
    csvs = []
    max_rows = 100000 # limit length at once 
    
    df = pd.DataFrame(**td_job)   
    while (len(df) > max_rows):
        d = df[:max_rows]
        r = df[max_rows:]
        csv = d.to_csv(header=True, index=False)
        csvs.append(csv)
        df = r

    if (len(df) > 0):
        csv = df.to_csv(header=True, index=False)
        csvs.append(csv)
      
    return csvs


def api_call(target_url, headers, files):
    res = requests.post(target_url, headers=headers, files=files)

    if res.status_code != 200: 
        logger.error(
            f"Failed to call Done API with http status code {res.status_code}"
        )
        raise Exception
    else:
        logger.info(
            f"Succeeded calling Done API with http status code {res.status_code}"
        )


def exec_main(
    sql: str,
    td_db: str,
    td_engine: str,
    target_url: str,
    filename: str
):
    logger.debug('*** Start ***')

    try:
        td_job = fetch_user_data(sql, td_db, td_engine)
        csvs = csv_out(td_job)

        for i, csv in enumerate(csvs):
            idx = i + 1
            files = {
                'file': (f'{filename}_{idx}.csv', csv, 'text/csv')
            }
            headers = {
                'Yappli-Token': os.environ["YAPPLI_TOKEN"]
            }
            api_call(target_url, headers, files)

            # wait 60m till next call when other files exist to be sent
            if csvs[idx:idx + 1]:
                logger.debug('*** Waiting till next call ***')
                time.sleep(60)

    except Exception:
        traceback.print_exc()
        sys.exit(1)

    finally:
        logger.debug('\n*** End ***')
