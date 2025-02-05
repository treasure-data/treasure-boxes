import os
import requests as req
import json
import pytd
import pandas as pd

def main():
    client = pytd.Client(
        apikey=os.getenv("API_KEY"), 
        endpoint=os.getenv("EP"), 
        database=os.getenv("ACT_DB"), 
        default_engine=os.getenv("ENGINE")
    )

    res = client.query('SELECT array_agg(DISTINCT riid) AS riids FROM ' + os.getenv("ACT_TBL"))
    df = pd.DataFrame(**res)
    riids = list(df.at[0, 'riids'])
    
    apiUsername = '<apiusername>'
    apiPassword = os.getenv("PW")
    campaignName = os.getenv("CAMP")
    
    # Get token
    tokenRes = req.post(
        'https://<clientid>-api.responsys.ocs.oraclecloud.com/rest/api/v1.3/auth/token',
        data={
            'user_name': apiUsername,
            'password': apiPassword,
            'auth_type': 'password'
        },
    )
    token = tokenRes.json()['authToken']
    endpoint = tokenRes.json()['endPoint']
    
    # Send batch data
    send_batches(campaignName, riids, endpoint, token)

def send_batches(campaignName, riids, endpoint, token):
    prod = os.environ.get('PROD', 'DEV').upper()
    batch_size = 200
    for i in range(0, len(riids), batch_size):
        recipients_batch = riids[i:i+batch_size]
        # Test mode
        if prod == 'DEV':
            print("---------------")
            print(i)
            print(recipients_batch)
            send_td(recipients_batch, campaignName)
        # Production Mode
        elif prod == 'PROD':
            # Activation to Oracle Responsys
            send(campaignName, recipients_batch, endpoint, token)
        # Other Mode
        else:
            print("Mode should be DEV or PROD")

def send(campaignName, riids_batch, endpoint, token):
    recipientsList = [{
        'recipient': {
            'recipientId': riid,
        }
    } for riid in riids_batch]
    
    print("-------------------")
    print(json.dumps({'recipientData': recipientsList}))
    
    print(endpoint + '/rest/api/v1.3/campaigns/' + campaignName + '/email')
    
    response = req.post(
        f'{endpoint}/rest/api/v1.3/campaigns/{campaignName}/email',
        data=json.dumps({'recipientData': recipientsList}),
        headers={
            'Authorization': token,
            'content-type': 'application/json',
        }
    )
    
    status_code = response.status_code
    res_text = response.text
    send_td(recipients_batch, campaignName, status_code=status_code, res_text=res_text)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
    else:
        print("Batch sent successfully!")
        print(response.json())
        

def send_td(recipients_batch, campaignName, **kwargs):
    td_log_database = 'activation_log'
    td_log_table = 'log_api'
    td_ingestion_endpoint = f'https://records.in.treasuredata.com/{td_log_database}/{td_log_table}'

    payload = {
        "ma": "Responsys",
        "campaign": campaignName,
        "status": kwargs.get('status_code', 200),
        "response": kwargs.get('res_text', 'sample test response message'),
        "recipients_batch": recipients_batch,
        "recipients_batch_size": len(recipients_batch),
        "activation_source": "Activation Actions"
    }
    headers = {
        "Content-Type": "application/vnd.treasuredata.v1.single+json",
        "Authorization": f"TD1 {os.environ['WRITE_KEY']}",
    }
    td_response = req.post(td_ingestion_endpoint, json=payload, headers=headers)
    print("Response from TD:", td_response.text)

if __name__ == "__main__":
    main()
