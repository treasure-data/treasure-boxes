import os
import sys
from urllib import parse

os.system(f"{sys.executable} -m pip install --upgrade pytd==1.4.0")

td_apikey = os.environ["TD_API_KEY"]
td_endpoint = os.environ["TD_ENDPOINT"]
skyfox_username = os.environ["SKYFOX_USERNAME"]
skyfox_password = os.environ["SKYFOX_PASSWORD"]
skyfox_auth_endpoint = os.environ["SKYFOX_AUTH_ENDPOINT"]
skyfox_endpoint = os.environ["SKYFOX_ENDPOINT"]
s3_accesskey = parse.unquote(os.environ["S3_ACCESSKEY"])
s3_secretkey = parse.unquote(os.environ["S3_SECRETKEY"])
session_unixtime = os.environ["SESSION_UNIXTIME"]


class Skyfox(object):
  def __init__(self):
    pass

  def get_token(self):
    import json, requests, digdag
  
    headers = {'Content-Type': 'application/json'}
    data = f'{{ "username": "{skyfox_username}", "password": "{skyfox_password}" }}'
    response = requests.post(f'https://{skyfox_auth_endpoint}/auth', headers=headers, data=data)
    assert response.ok, f"Status Code : {response.status_code} | {response.text}"
  
    digdag.env.store({'token': json.loads(response.text)['token']})


  def upload(self, bucket, path, job_id):
    import json, requests, digdag
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
    
    data = json.dumps({ 
      "source": {
        "type": "S3", 
        "parameter": { 
          "name": path, 
          "awsAccessKeyId": s3_accesskey, 
          "awsSecretAccessKey": s3_secretkey, 
          "bucketName": bucket, 
          "objectKey": path 
        } 
      }, 
      "note": f"Upload training data set at s3://{bucket}/{path} | JobID of TD is {job_id}"
    })
    response = requests.post(f'https://{skyfox_endpoint}/data', headers=headers, data=data)
      
    assert response.ok, f"Status Code : {response.status_code} | {response.text}"
  
    data_id = json.loads(response.text)['id']
    digdag.env.store({'data_id': data_id})
  
    self._check_completed_uploading_data(data_id)
  
  
  def _check_completed_uploading_data(self, id, seconds=60):
    import json, requests, digdag
    import time
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
  
    # Wait until uploading data finishes
    while 1:
      response = requests.get(f'https://{skyfox_endpoint}/data/{id}', headers=headers)
      status = json.loads(response.text)['status']
      if status == 'uploaded':
        break
      elif status == 'failure':
        raise ValueError("[ERROR] Something is wrong.")
      else:
        time.sleep(seconds)
      
    return True
  
  
  def train(self, data_id, target_variable, transformer_id='Q5w0W1VJ0Kv7OJ4m', algorithm_id=25):
    import json, requests, digdag
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
    
    data = json.dumps({ 
      "dataId": data_id,
      "name": f"Training model with {data_id}",
      "objectiveVariable": target_variable,
      "transformerBundleId": transformer_id,
      "algorithmId": algorithm_id,
      "algorithmSetting": {
        "hyperParameter": {},
        "opitons": {}
      },
      "note": f"Build model with {data_id}"
    })
    response = requests.post(f'https://{skyfox_endpoint}/models', headers=headers, data=data)
      
    assert response.ok, f"Status Code : {response.status_code} | {response.text}"
  
    model_id = json.loads(response.text)['id']
    digdag.env.store({'model_id': model_id})
  
    self._check_completed_building_model(model_id)
  
  
  def _check_completed_building_model(self, id, seconds=60):
    import json, requests, digdag
    import time
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
  
    # Wait until building model finishes
    while 1:
      response = requests.get(f'https://{skyfox_endpoint}/models/{id}', headers=headers)
      status = json.loads(response.text)['status']
      if status == 'complete':
        break
      elif status == 'xxxx':
        raise ValueError("[ERROR] Something is wrong.")
      elif status == 'processing':
        time.sleep(seconds)
      else:
        time.sleep(seconds)
      
    return True


  def predict(self, data_id, model_id, dest_database, dest_table):
    import json, requests, digdag
    import pandas as pd
    import pytd
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
    
    data = json.dumps({ 
      "dataId": data_id,
      "deleteData": False,
      "options": {
        "withInput": True
        }
    })
    response = requests.post(f'https://{skyfox_endpoint}/models/{model_id}/predictions', headers=headers, data=data)
      
    prediction_id = json.loads(response.text)['id']
    assert response.ok, f"Status Code : {response.status_code} | {response.text}"
  
    response = self._check_completed_predicting(model_id, prediction_id)

    results = pd.DataFrame(json.loads(response.text)['results'])
    
    client = pytd.Client(apikey=td_apikey, endpoint=td_endpoint)
    client.load_table_from_dataframe(results.assign(time=session_unixtime), f'{dest_database}.{dest_table}', if_exists='append')

    return True
  
  
  def _check_completed_predicting(self, model_id, prediction_id, seconds=60):
    import json, requests, digdag
    import time
  
    token = digdag.env.params['token']
  
    headers = {
        'skyfox-api-access-token': token,
        'Content-Type': 'application/json',
    }
  
    # Wait until building model finishes
    while 1:
      response = requests.get(f'https://{skyfox_endpoint}/models/{model_id}/predictions/{prediction_id}', headers=headers)
      status = json.loads(response.text)['status']
      if status == 'complete':
        break
      elif status == 'failure':
        raise ValueError("[ERROR] Something is wrong.")
      elif status == 'processing':
        time.sleep(seconds)
      else:
        time.sleep(seconds)
      
    return response
