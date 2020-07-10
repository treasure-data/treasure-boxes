import pandas as pd
import pytd
import os
import sys
import requests
from logging import INFO, StreamHandler, getLogger
import gzip

os.system(f"{sys.executable} -m pip install -U pytd==1.3.0 td-client")

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


def upload(sqlfile, database, presigned_url):
    with open(sqlfile) as f:
        querytxt = f.read()

    client = pytd.Client(apikey=os.getenv("td_apikey"), database=database)
    res = client.query(querytxt)
    df = pd.DataFrame(**res)
    csv = df.to_csv(header=False, index=False, sep="\t")

    logger.info("---- user list as first 10 lines----")
    logger.info("\n".join(csv.splitlines()[:10]))
    logger.info("---- Total number of IDs = " + str(len(csv.splitlines())) + "----")

    res = requests.put(
        presigned_url,
        data=gzip.compress(bytes(csv, "utf-8")),
        headers={"Content-Encoding": "gzip"},
    )

    if res.status_code != 200:
        logger.error(
            f"Failed to call Yahoo API with http status code {res.status_code}"
        )
        logger.error(res.text)
        sys.exit(os.EX_DATAERR)
    else:
        logger.info(
            f"Succeeded calling Yahoo API with http status code {res.status_code}"
        )
