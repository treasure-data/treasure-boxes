import requests
import json
import os

# The below variable should contain the master API key of the console of the source Master segment
source_master_api_key = os.environ.get('TD_SOURCE_API_MASTER_KEY')

# the below variable should contain the master segment number (in string format like '010101') of the source Master segment
source_ms_num = os.environ.get('SOURCE_MS_NUMBER')

# the below variable should contain the master segment number (in string format like '010101') of the source Master segment
destination_ms_num = os.environ.get('DEST_MS_NUMBER')

# The below variable should contain the master API key of the destination console
# demodata for now 
destination_master_api_key = os.environ.get('TD_DEST_API_MASTER_KEY')

# the below API fetches the details and schema of the source master segment 
source_headers = {
    'Authorization': 'TD1 '+source_master_api_key
}
source_segments = requests.get('https://api-cdp.treasuredata.com/audiences/'+source_ms_num+'/segments/', headers=source_headers)

# the API response is stored as json
source_segments = source_segments.json()

# the total number of segments is printed
print('total number of all segments:',len(source_segments))

destination_headers = {
    'Authorization': 'TD1 '+destination_master_api_key,
    'content-type': 'application/json'
}

def execute():
  # the below loop iterates through all the source segments, creates a json payload for each, and calls the segment creation API in the destination console.
  if (len(source_segments)) > 0:
      for segment in source_segments:
          
          #get folder id a original segment
          folder_id = segment['segmentFolderId']

          #get folder information from api to get folder name and description 
          folder_req = requests.get(f'https://api-cdp.treasuredata.com/audiences/{source_ms_num}/folders/{folder_id}', headers=source_headers)
          folder_to_copy = folder_req.json()

          # Request by Rhett to allow migration of a single folder
          if folder_to_copy['name'] != os.environ.get('SEG_FOLDER_NAME'):
              continue

          new_folder = {}
          new_folder['name'] = folder_to_copy['name']
          new_folder['description'] = folder_to_copy['description']
          #try to create the folder in the new master segment
          try: 
              post_ = requests.post(f'https://api-cdp.treasuredata.com/audiences/{destination_ms_num}/folders/', headers=destination_headers, json=new_folder)
          except Exception as e: 
              print(e)
          #if the attempt to create a new folder returns with 400 it means that the folder already exists with that name
          #in this case get the folder id (we will add the segment to this folder)
          if post_.status_code == 400: 
              folders = requests.get(f'https://api-cdp.treasuredata.com/audiences/{destination_ms_num}/folders/', headers=destination_headers)
              folder_id = next(folder['id'] for folder in folders.json() if folder["name"] == new_folder['name'])
          #if the attempt is succesful get the folder id of the newly created folder
          else: 
              folder_id = post_.json()['id']

          json_payload = {
              'audienceId': segment['audienceId'],
              'name': segment['name'],
              'realtime': segment['realtime'],
              'description': segment['description'],
              'kind': segment['kind'],
              'rule': segment['rule'],
              'segmentFolderId': folder_id
          }

          segment_creation = requests.post('https://api-cdp.treasuredata.com/audiences/'+destination_ms_num+'/segments',headers=destination_headers, data=json.dumps(json_payload))
          segment_creation = segment_creation.json()
          print('segment copied')

  print('MS Folder Copy Complete')
