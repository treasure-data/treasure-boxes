# CSV Query Result Download
# Query by pandas-td
# Download by pandas

import os

# Install Libs
print('Installing Libs ...')
os.system("pip install --upgrade pip")
os.system("pip install pandas-td")
os.system("pip install td-client")

# Set Params
print('Setting Params ...')
endpoint='https://api.treasuredata.com'
td_apikey = os.environ.get('td_apikey')
dbname = 'sample_datasets'
query = 'SELECT time, host, path FROM www_access LIMIT 100'
session_time_unixtime = 1536070106

def input_query_result_pd(dbname, query, engine_type):
  import pandas_td as td

  # Connect TD
  con = td.connect(td_apikey, endpoint)
  engine = con.query_engine(database=dbname, type=engine_type)

  # Execute query
  print('Executing query ...')
  df = td.read_td(query, engine)
  print(df)


def run_query(dbname, query, engine_type):
  import tdclient
  
  with tdclient.Client(td_apikey) as td:
    job = td.query(dbname, query, type=engine_type)
  
  print("Submitted job .. job_id: " + str(job.job_id))

  # Sleep until job's finish
  job.wait()
  print("job finished")
    
  return job

def run_saved_query(query_name, session_time_unixtime):
  import tdclient
  
  with tdclient.Client(td_apikey) as td:
    results = td.run_schedule(query_name, session_time_unixtime, 1)
  
  print("Submitted job .. job_id: " + str(results[0].id))
  job = td.job(results[0].id)
  
  # Sleep until job's finish
  job.wait()
  print("job finished")
    
  return job


def input_result(job):
  import pandas
  
  if job.status() != u'success':
     print('not success')
     raise
     
  result_header_array = []
  for (col,type) in job.result_schema:
    result_header_array.append(col)
  
  result_array = []
  for row in job.result():
    result_array.append(row)

  df = pandas.DataFrame(result_array, columns=result_header_array)
  print(df)


def main():
  input_query_result_pd(dbname, query, 'presto')
  job = run_query(dbname, query, 'presto')
  input_result(job)
  job = run_saved_query('noda1', session_time_unixtime)
  input_result(job)
  

