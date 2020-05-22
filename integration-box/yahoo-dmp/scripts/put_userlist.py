import os
import sys
import requests

os.system(f"{sys.executable} -m pip install -U pytd==1.3.0 td-client")
import pytd
import pandas as pd

def upload(sqlfile, database, presigned_url):
  with open(sqlfile) as f:
    querytxt = f.read()

  client = pytd.Client(apikey=os.getenv('td_apikey'), database=database)
  res = client.query(querytxt)
  df = pd.DataFrame(**res)
  csv = df.to_csv(index=False)

  requests.put(presigned_url, data=csv)
