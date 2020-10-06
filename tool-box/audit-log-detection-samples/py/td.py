import os, sys
import requests
import digdag

apikey = os.environ['TD_API_KEY']
endpoint = os.environ['TD_ENDPOINT']


def get_users():
  headers = {
    'AUTHORIZATION': f'TD1 {apikey}',
  }
  response = requests.get(f'https://{endpoint}/v3/user/list', headers=headers)
  digdag.env.store({'users': response.content.decode()})
  return True  
