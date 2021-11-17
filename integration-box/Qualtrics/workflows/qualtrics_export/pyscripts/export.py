import os, sys
import json
import pytd
import requests

print(f'starting up')

# Qualtrics settings
qualtrics_apikey = os.environ['QUALTRICS_API_KEY']
qualtrics_endpoint = os.environ['QUALTRICS_ENDPOINT']
qualtrics_aid = os.environ['QUALTRICS_AID']

# TD settings
apikey = os.environ['TD_API_KEY']
endpoint = os.environ['TD_API_SERVER']
timezone = os.environ['TD_DATA_TIMEZONE'] or 'UTC'
db = os.environ['db']
table = os.environ['table']
columns_array = json.loads(os.environ['columns'])
delimiter = ',' # fixed: user should set comma as delimiter in Qualtrics Automation settings

select_columns = []
csv_file_headers = []

def main():

  print(f'Automation ID is {qualtrics_aid}')

  for col in columns_array:
    
    # create columns list for select clause
    # col format: [TD column name, File column header, Qualtrics column type]

    # if coltype is Transaction Data, assume the col in TD is timestamp and convert it to ISO-8601 timestamp (2006-01-02T15:04:05+07:00)
    if len(col) == 3 and col[2] == 'Transaction':
      select_columns.append(f"to_iso8601(from_unixtime(td_time_parse({col[0]}, '{timezone}')))")
    else:
      select_columns.append(col[0])
    
    # create header for the exporting csv file
    csv_file_headers.append(col[1])
  
  columns = ','.join(select_columns)

  print(f'select columns {columns}')
  print(f'csv file headers {csv_file_headers}')

  # internal settings
  file_path = os.path.expanduser('~/user_list.txt')

  # TODO: variables checks

  # Extract data from TD
  extracted_data = extract_data(db, table, columns, apikey, endpoint)

  # Save extracted data as CSV file
  save_list_as_file(file_path, extracted_data, csv_file_headers, delimiter)

  # Send the saved CSV file to Qualtrics
  send_to_qualtrics(qualtrics_apikey, qualtrics_endpoint, qualtrics_aid, file_path)
  
  print('DONE')


def extract_data(db, table, cols, apikey, endpoint):
  print(f'\nextracting data from {db}.{table}')

  client = pytd.Client(apikey = apikey, endpoint = endpoint, database = db)
  res = client.query(f'select {cols} from {db}.{table}')

  print(f'{len(res["data"])} rows extracted')
  return res['data']

def save_list_as_file(file_path, list, header, delimiter):
  print(f'\nsaving extracted data as CSV file to {file_path}')

  content = delimiter.join(header) + '\n'
  for line in list:
    content += delimiter.join(item or '' for item in line) + '\n'

  with open(file_path, 'w') as f:
    f.write(content)
    print('content successfully written')


def send_to_qualtrics(qualtrics_apikey, qualtrics_endpoint, qualtrics_aid, file_path):
  print(f'\nsending file to Qualtrics File Service {qualtrics_endpoint}')

  url = os.path.join(qualtrics_endpoint, 'automations-file-service/automations', qualtrics_aid, 'files')
  headers = {'X-API-TOKEN': qualtrics_apikey}
  files = {'file': open(file_path,'rb')}

  r = requests.post(url, headers=headers, files=files)
  if r.ok == False:
    print(r.reason)
    print(r.text)
    sys.exit(f'Request failed')

  print(r)
  print(f'{r.status_code} file successfully sent to Qualtrics')

