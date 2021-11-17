import os, sys
import json
import time
import pandas as pd
import pytd
import requests

print(f'starting up')

# Qualtrics settings
qualtrics_apikey = os.environ['QUALTRICS_API_KEY']
qualtrics_endpoint = os.environ['QUALTRICS_ENDPOINT']
qualtrics_sid = os.environ['QUALTRICS_SURVEYID']
qualtrics_embedded_data_labels = list(map(lambda x: x.strip().lower(), os.environ['QUALTRICS_EMBEDDED_DATA_LABELS'].split(',')))
qualtrics_default_fixed_data_labels = ['solutionrevision', 'projectcategory', 'projecttype']

# TD settings
apikey = os.environ['TD_API_KEY']
endpoint = os.environ['TD_API_SERVER']
convert_to_long = True if os.environ['TD_CONVERT_TO_LONG'].lower() == 'true' else False
db = os.environ['TD_DB']
table = os.environ['TD_TABLE']
if_exists = os.environ['TD_IF_EXISTS'] or 'append'

# local settings
local_file_path = os.path.expanduser('~/result.csv')


def main():

  # [Qualtrics] Start Response Export
  # https://api.qualtrics.com/api-reference/b3A6NjEwMzk-start-response-export
  # Command Qualtrics to prepare export data
  # outcome: progressId

  print(f'*** [Qualtrics] Start Response Export')
  print(f'Survey ID is {qualtrics_sid}')

  start_response_report_url = os.path.join(qualtrics_endpoint, f'API/v3/surveys/{qualtrics_sid}/export-responses')
  headers = {
    'X-API-TOKEN': qualtrics_apikey,
    'Content-Type': 'application/json'
  }
  # Export settings
  # export data timezone is UTC
  data = json.dumps({
    'format': 'csv', # fixed value for this workflow
    'compress': 'false' # fixed value for this workflow
  })
  
  print(f'GET {start_response_report_url}')
  r = requests.post(start_response_report_url, headers=headers, data=data)
  print(f'Response status code {r.status_code}')
  
  if r.ok == False:
    print(r.reason)
    print(r.text)
    sys.exit(f'Request failed')

  print(f'response content {r.text}')

  response = r.json()
  progressId = response['result']['progressId']
  print(f'successfully received progressId {progressId}')


  # [Qualtrics] Get Response Export Progress
  # https://api.qualtrics.com/api-reference/b3A6NjEwNDE-get-response-export-progress
  # Get progress status for the progressId
  # outcome: fileId when complete

  print(f'*** [Qualtrics] Get Response Export Progress')

  get_response_report_progress_url = os.path.join(qualtrics_endpoint, f'API/v3/surveys/{qualtrics_sid}/export-responses/{progressId}')
  fileId = None

  # Progress check runs 30 seconds after start exporting
  # after that every 60 seconds
  while True:

    time.sleep(30)
    
    print(f'GET {get_response_report_progress_url}')
    r = requests.get(get_response_report_progress_url, headers=headers)
    print(f'Response status code {r.status_code}')
  
    if r.ok == False:
      print(r.reason)
      print(r.text)
      sys.exit(f'Request failed')

    print(f'response content {r.text}')

    response = r.json()
    if response['result']['status'] != 'inProgress':
      fileId = response['result']['fileId']
      break

    time.sleep(30)

  print(f'successfully received fileId {fileId}')


  # [Qualtrics] Get Response Export File
  # https://api.qualtrics.com/api-reference/b3A6NjEwNDM-get-response-export-file
  # Download the generated file

  print(f'*** [Qualtrics] Get Response Export File')

  get_response_export_file_url = os.path.join(qualtrics_endpoint, f'API/v3/surveys/{qualtrics_sid}/export-responses/{fileId}/file')

  print(f'GET {get_response_export_file_url}')
  r = requests.get(get_response_export_file_url, headers=headers)
  print(f'Response status code {r.status_code}')

  if r.ok == False:
    print(r.reason)
    print(r.text)
    sys.exit(f'Request failed')

  print(f'export file downloaded')

  # write the downloaded file to local
  with open(local_file_path, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
      fd.write(chunk)
  
  print(f'downloaded file is saved as {local_file_path}')


  # import csv file to TD
  # open the csv file to construct pandas DataFrame

  print(f'*** csv file processing')

  # skip rows 0 and 1 of the file, take row 2 (prop 'ImportId') as header string
  df = pd.read_csv(local_file_path, skiprows=[0,1], keep_default_na=False)

  print(f'csv file read: {len(df)} rows')
  print(f'original header row in the exported file: {list(df.columns)}')

  # rename column header by extracting ImportID
  renamed_cols = list(map(lambda x: json.loads(x)['ImportId'].lower(), df.columns))
  df.columns = renamed_cols

  # if converting to long format (convert_to_long is false)
  if convert_to_long == True:
    print('*** Converting data to long format (convert_to_long == True)')

    # add user-supplied embedded data lables to columns to keep wide
    embedded_data_cols = set(renamed_cols).intersection(set(map(lambda x: x.lower(), qualtrics_embedded_data_labels)))

    # default 'solutionrevision', 'projectcategory', 'projecttype'
    default_data_cols = set(renamed_cols).intersection(set(qualtrics_default_fixed_data_labels))

    # extract fixed cols (userLanguage and all columns that come before it)
    fixed_cols = set(renamed_cols[:renamed_cols.index('userlanguage') + 1])
    fixed_cols |= embedded_data_cols
    fixed_cols |= default_data_cols
    print(f'columns not to be converted to long format: {fixed_cols}')

    # convert wide to long format
    df = df.melt(fixed_cols, var_name='question')
    print(f'wide data converted to long format: {len(df)} rows in total')
  
  else:
    print('*** Importing data in wide format (convert_to_long != True)')

  # add surveyid as column
  df['survey_id'] = qualtrics_sid

  print(f'columns to be imported to TD: {list(df.columns)}')
  
  client = pytd.Client(apikey=apikey, endpoint=endpoint, database=db, default_engine='presto')

  # create destination table if not exists
  print(f'*** [TD] creating table if not exists {db}.{table}')

  headers = { 'Authorization': f'TD1 {apikey}' }
  r = requests.post(f'{endpoint}/v3/table/create/{db}/{table}', headers=headers)
  print(f'API response status code {r.status_code}')
  if r.status_code != 200:
    print(r.content)

  # add column survey_id to the destination table if not exists
  # the following delete operation will fail if this is not done
  print(f'*** [TD] adding column \'survey_id\' to {db}.{table}')

  r = requests.post(f'{endpoint}/v3/table/update/{db}/{table}?schema=%5B%5B%22survey_id%22%2C%22string%22%5D%5D', headers=headers)
  print(f'API response status code {r.status_code}')
  if r.status_code != 200:
    print(r.content)

  # delete survey data for the survey_id from the current table
  print(f'*** [TD] deleting existing data for survey_id {qualtrics_sid} from {db}.{table}')

  result = client.query(f'delete from {db}.{table} where survey_id = \'{qualtrics_sid}\'')
  print(result)


  # append the new data

  print(f'*** [TD] starting bulk import to {db}.{table}')
  client.load_table_from_dataframe(df, table, writer='bulk_import', if_exists=if_exists, fmt='msgpack')
  print(f'*** done')
