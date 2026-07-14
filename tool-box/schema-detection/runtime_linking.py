def use_df():
    import sys
    import os
    import digdag
    sys.path.append('/home/td-user/.local/lib/python3.6/site-packages')
    os.system(f"{sys.executable} -m pip install --user pandas")
    os.system(f"{sys.executable} -m pip install --user -U git+https://github.com/treasure-data/pytd#egg=pytd[spark]")
    os.system(f"{sys.executable} -m pip install --user time")
    os.system(f"{sys.executable} -m pip install --user pyyaml")
    os.system(f"{sys.executable} -m pip install --user json")
    os.system(f"{sys.executable} -m pip install --user requests")
    os.system(f"{sys.executable} -m pip install --user digdag")
    import time
    import yaml
    import pandas as pd
    import pytd
    import tdclient
    import json
    import requests
  
    class InConnector:
        apikey = os.environ['apikey']
        def __init__(self):
            self.apikey = os.environ['apikey']
    
        def convert_to_dict(self,seed_file):
            with open(seed_file, 'r') as f:
                self.payload = yaml.safe_load(f)
            return self.payload
    
        def connector_guess(self, job):

            headers = {"content-type": "application/json; charset=utf-8","authorization":"TD1 "your apikey""}
            payload = json.dumps(job).encode("utf-8") if isinstance(job, dict) else job
            print(payload)
            with requests.post("https://api.treasuredata.com/v3/bulk_loads/guess", payload, headers=headers) as res:
                code,body = res.status_code,res.content
               # print(body)
            if code != 200:
                    print("DataConnector job preview failed", res, body)
            return body.decode("utf-8")
        
        def change_to_string(self, body):
            body =  json.loads(body)
            list_of_col = body['config']['in']['parser']['columns']
            for i in range(len(list_of_col)):
                if list_of_col[i]['type'] != 'string':
                    list_of_col[i]['type'] = 'string'
                try:
                    del list_of_col[i]['format']
                except:
                    continue
            return (body)

        
        def write_schema(self,body,payload):
            list_of_col = body['config']['in']['parser']['columns']
            df = pd.DataFrame(list_of_col,columns = ['name','type'])
            dest_table = payload['out']['table']
            try:
                with tdclient.connect(db='demo_schema', type='presto', wait_callback='on_waiting',apikey=InConnector.apikey) as td:
                    val = pd.read_sql('select count(*) as cnt from {} where time in (select max(time) from {})'.format(dest_table,dest_table), td)
                    prev_col = val['cnt'][0]
                if prev_col - len(df) !=0:
                    print('Schema Changed from last run')
                    digdag.env.store({'change_status': 'true'})
                    client = pytd.Client(apikey=InConnector.apikey, endpoint='https://api.treasuredata.com/', database='database_name')
                    client.load_table_from_dataframe(df,dest_table, writer='bulk_import', if_exists='overwrite')
                else:
                    print('No Change detected')
                    digdag.env.store(({'change_status': 'false'}))
                    client = pytd.Client(apikey=InConnector.apikey, endpoint='https://api.treasuredata.com/', database='database_name')
            except:
                client = pytd.Client(apikey=InConnector.apikey, endpoint='https://api.treasuredata.com/', database='database_name')
                client.load_table_from_dataframe(df,dest_table, writer='bulk_import', if_exists='overwrite')     
            
     
        
    
    
    test = InConnector()
    a = test.convert_to_dict('config-s3.yml')
    b = test.connector_guess(a)
    c = test.change_to_string(b)
    test.write_schema(c,a)
 
   
    

    
    
