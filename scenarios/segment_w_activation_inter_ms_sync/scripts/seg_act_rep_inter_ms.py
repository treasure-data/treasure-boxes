#scripts/seg_act_rep_inter_ms.py
import os
import requests

def main(**kwargs):
  # Init
  td_api_key = os.getenv("TD_API_KEY")
  audience_api_ep = kwargs.get("aud_api_ep")
  source_audience_id = str(os.getenv("AUDIENCE_ID"))
  target_audience_ids = kwargs.get("target_audience_ids")
  source_segment_id = str(os.getenv("SEGMENT_ID"))
  source_activation_id = str(os.getenv("ACTIVATION_ID"))
  get_segment_path = "/audiences/{audienceId}/segments/{segmentId}"
  get_activation_path = "/audiences/{audienceId}/segments/{segmentId}/syndications/{syndicationId}"
  get_folder_path = "/entities/folders/{folderId}"
  get_list_of_assets = "/entities/by-folder/{folderId}"
  get_folder_list_path = "/audiences/{audienceId}/folders"
  get_segment_list_path = "/audiences/{audienceId}/folders/{folderId}/segments"
  get_segment_list_in_parent_segment = "/audiences/{audienceId}/segments"
  post_folder_path = "/entities/folders"
  post_new_segment_path = "/audiences/{audienceId}/segments"
  post_new_activation_path = "/audiences/{audienceId}/segments/{segmentId}/syndications"

  # Get source segment json data
  def get_source_segment():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_source_segment_path = audience_api_ep + get_segment_path.replace("{audienceId}", source_audience_id).replace("{segmentId}", source_segment_id)
    source_segment = requests.request("GET", get_source_segment_path, headers = headers, data = payload)

    if source_segment.status_code == 200:
      source_segment_json = source_segment.json()
    else:
      print(f"Failed to fetch source segment. Status code: {source_segment.status_code} - {source_segment.reason} - {source_segment.text}")
      exit()

    return source_segment_json

  # Get segment json data by id
  def get_segment_by_id(segment_id):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_segment_by_id_path = audience_api_ep + get_segment_path.replace("{audienceId}", source_audience_id).replace("{segmentId}", segment_id)
    referenced_segment = requests.request("GET", get_segment_by_id_path, headers = headers, data = payload)

    if referenced_segment.status_code == 200:
      referenced_segment_json = referenced_segment.json()
    else:
      print(f"Failed to fetch referenced segment. Status code: {referenced_segment.status_code} - {referenced_segment.reason} - {referenced_segment.text}")
      exit()

    return referenced_segment_json

  # Get target segment id
  def get_target_segment_id(segment_target_folder_id, source_segment_name):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_target_segment_list_path = audience_api_ep + get_segment_list_path.replace("{audienceId}", target_audience_id).replace("{folderId}", segment_target_folder_id)
    target_segment_list = requests.request("GET", get_target_segment_list_path, headers = headers, data = payload)

    if target_segment_list.status_code == 200:
      target_segment_list_json = target_segment_list.json()
      target_segment = next((item for item in target_segment_list_json if item["name"] == source_segment_name), None)
      target_segment_id = target_segment["id"]
    else:
      print(f"Failed to fetch target segment. Status code: {target_segment_list.status_code} - {target_segment_list.reason} - {target_segment_list.text}")
      exit()
    
    return target_segment_id

  # Get source activation json data
  def get_source_activation():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_source_activation_path = audience_api_ep + get_activation_path.replace("{audienceId}", source_audience_id).replace("{segmentId}", source_segment_id).replace("{syndicationId}", source_activation_id)
    source_activation = requests.request("GET", get_source_activation_path, headers = headers, data = payload)

    if source_activation.status_code == 200:
      source_activation_json = source_activation.json()
    else:
      print(f"Failed to fetch source activation. Status code: {source_activation.status_code} - {source_activation.reason} - {source_activation.text}")
      exit()

    return source_activation_json

  # Get source folder json data
  def get_source_folder(source_segment_json):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    source_folder_id = source_segment_json["segmentFolderId"]
    get_source_folder_path = audience_api_ep + get_folder_path.replace("{folderId}", source_folder_id)
    source_folder = requests.request("GET", get_source_folder_path, headers = headers, data = payload)

    if source_folder.status_code == 200:
      source_folder_json = source_folder.json()
    else:
      print(f"Failed to fetch source folder. Status code: {source_folder.status_code} - {source_folder.reason} - {source_folder.text}")
      exit()

    return source_folder_json

  # Get folder json data by id
  def get_folder_by_id(folder_id):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_folder_by_id_path = audience_api_ep + get_folder_path.replace("{folderId}", folder_id)
    referenced_segment_folder = requests.request("GET", get_folder_by_id_path, headers = headers, data = payload)

    if referenced_segment_folder.status_code == 200:
      referenced_segment_folder_json = referenced_segment_folder.json()
    else:
      print(f"Failed to fetch referenced segment folder. Status code: {referenced_segment_folder.status_code} - {referenced_segment_folder.reason} - {referenced_segment_folder.text}")
      exit()

    return referenced_segment_folder_json

  # Get source parent folder json data
  def get_source_parent_folder(source_folder_json):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    parent_folder_id = source_folder_json["data"]["relationships"]["parentFolder"]["data"]["id"]
    get_parent_folder_path = audience_api_ep + get_folder_path.replace("{folderId}", parent_folder_id)
    parent_folder = requests.request("GET", get_parent_folder_path, headers = headers, data = payload)

    if parent_folder.status_code == 200:
      parent_folder_json = parent_folder.json()
    else:
      print(f"Failed to fetch parent folder. Status code: {parent_folder.status_code} - {parent_folder.reason} - {parent_folder.text}")
      exit()

    return parent_folder_json

  # Get target master segment folders json data
  def get_target_master_segment_folders():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_target_master_segment_folders_path = audience_api_ep + get_folder_list_path.replace("{audienceId}", target_audience_id)
    target_master_segment_folders = requests.request("GET", get_target_master_segment_folders_path, headers = headers, data = payload)

    if target_master_segment_folders.status_code == 200:
      target_master_segment_folders_json = target_master_segment_folders.json()
    else:
      print(f"Failed to fetch target master segment. Status code: {target_master_segment_folders.status_code} - {target_master_segment_folders.reason} - {target_master_segment_folders.text}")
      exit()
    
    return target_master_segment_folders_json

  # Get a list of assets under a given folder as json data
  def get_assets_in_folder(target_segment_folder_id):
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_assets_in_folder_path = audience_api_ep + get_list_of_assets.replace("{folderId}", target_segment_folder_id)
    asset_list = requests.request("GET", get_assets_in_folder_path, headers = headers, data = payload)
    
    if asset_list.status_code == 200:
      asset_list_json = asset_list.json()
    else:
      print(f"Failed to fetch asset list. Status code: {asset_list.status_code} - {asset_list.reason} - {asset_list.text}")
      exit()

    return asset_list_json

  # Get segment list in target parent segment
  def get_segments_in_parent_segment():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    get_segment_list_in_parent_segment_path = audience_api_ep + get_segment_list_in_parent_segment.replace("{audienceId}", target_audience_id)
    target_segments = requests.request("GET", get_segment_list_in_parent_segment_path, headers = headers, data = payload)

    if target_segments.status_code == 200:
      target_segments_json = target_segments.json()
    else:
      print(f"Failed to fetch target segments. Status code: {target_segments.status_code} - {target_segments.reason} - {target_segments.text}")
      exit()

    return target_segments_json

  # Look up all segments within a given folder, and extract the found segment's id
  def get_segment_id_in_folder(target_segment_folder_id, referenced_segment_name):
    target_segment_id = next((item["id"] for item in get_assets_in_folder(target_segment_folder_id)["data"] if item["attributes"]["name"] == referenced_segment_name), None)

    return target_segment_id

  # Post new folder
  def post_target_folder(source_folder_name, source_folder_description, segment_target_parent_folder_id):
    payload = {
      "type": "folder-segment",
      "attributes": {
          "name": source_folder_name,
          "description": source_folder_description
      },
      "relationships": {
          "parentFolder": {
              "data": {
                  "id": segment_target_parent_folder_id,
                  "type": "folder-segment"
              }
          }
      }
    }
    headers = {
        "Authorization": f"TD1 {td_api_key}",
        "Content-Type": "application/json"
    }
    new_folder = requests.request("POST", audience_api_ep + post_folder_path, headers = headers, json = payload)
    if new_folder.status_code == 200:
      print(f"'{source_folder_name}' folder was synced to '{target_audience_id}' successfully!")
      new_folder_response_json = new_folder.json()
      target_folder_id = new_folder_response_json["data"]["id"]
    else:
      print(f"Failed to post folder: '{source_folder_name}' - Status code: {new_folder.status_code} - {new_folder.reason} - {new_folder.text}")
      exit()
    
    return target_folder_id

  # Post new segment
  def post_target_segment(source_segment_json, segment_target_folder_id):
    existing_segment_rules = extract_existing_segment_rules(source_segment_json)
    # If there are any "Existing Segment" rules in the source segment's rules
    if len(existing_segment_rules) > 0:
      rules = replace_existing_segment_rules(source_segment_json, existing_segment_rules)
    else:
      rules = source_segment_json["rule"]

    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    payload = {
      "audienceId": target_audience_id,
      "name": source_segment_json["name"],
      "realtime": source_segment_json["realtime"],
      "isVisible": source_segment_json["isVisible"],
      "kind": source_segment_json["kind"],
      "description": source_segment_json["description"],
      "segmentFolderId": segment_target_folder_id,
      "rule": rules,
    }
    new_segment = requests.request("POST", audience_api_ep + post_new_segment_path.replace("{audienceId}", target_audience_id), headers = headers, json = payload)
    if new_segment.status_code == 200:
      print(f"'{source_segment_json["name"]}' segment was synced to '{target_audience_id}' successfully!")
      new_segment_response_json = new_segment.json()
      target_segment_id = new_segment_response_json["id"]
      post_target_activation(get_source_activation(), target_segment_id)
    elif new_segment.status_code == 400:
      post_target_activation(get_source_activation(), get_target_segment_id(segment_target_folder_id, source_segment_json["name"]))
    else:
      print(f"Failed to post segment - Status code: {new_segment.status_code} - {new_segment.reason} - {new_segment.text}")
      exit()

  # Post activation to new segment
  def post_target_activation(source_activation_json, target_segment_id):
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    payload = {
      "type": "syndication",
      "segmentId": target_segment_id,
      "name": source_activation_json["name"],
      "activationTemplateId": source_activation_json["activationTemplateId"],
      "allColumns": source_activation_json["allColumns"],
      "connectionId": source_activation_json["connectionId"],
      "description": source_activation_json["description"],
      "scheduleType": source_activation_json["scheduleType"],
      "scheduleOption": source_activation_json["scheduleOption"],
      "repeatSubFrequency": source_activation_json["repeatSubFrequency"],
      "timezone": source_activation_json["timezone"],
      "notifyOn": source_activation_json["notifyOn"],
      "emailRecipients": source_activation_json["emailRecipients"],
      "connectorConfig": source_activation_json["connectorConfig"],
      "audienceId": target_audience_id,
      "columns": source_activation_json["columns"],
    }
    activation_name = source_activation_json["name"]
    new_activation = requests.request("POST", audience_api_ep + post_new_activation_path.replace("{audienceId}", target_audience_id).replace("{segmentId}", target_segment_id), headers = headers, json = payload)
    if new_activation.status_code == 200:
      print(f"'{activation_name}' activation was synced to '{target_audience_id}' successfully!")
    else:
      print(f"Failed to post activation - Status code: {new_activation.status_code} - {new_activation.reason} - {new_activation.text}")
      exit()

  # Extract "Existing Segment" rules from segment rules
  def extract_existing_segment_rules(source_segment_json):
    existing_segment_rules = []
    if isinstance(source_segment_json, dict):
      # Check if this dict itself is a Reference node
      if source_segment_json.get("type") == "Reference":
        existing_segment_rules.append(source_segment_json)
      # Recurse into all values
      for value in source_segment_json.values():
        existing_segment_rules.extend(extract_existing_segment_rules(value))
    elif isinstance(source_segment_json, list):
      for item in source_segment_json:
        existing_segment_rules.extend(extract_existing_segment_rules(item))

    return existing_segment_rules

  # Find and replace the source referenced segment id with the target one
  def replace_referenced_segment_id(referenced_segment_id, target_referenced_segment_id, source_segment_json):
    stack = [source_segment_json["rule"]]

    while stack:
      current = stack.pop()
      if isinstance(current, dict):
        if current.get("type") == "Reference" and str(current.get("id")) == str(referenced_segment_id):
          current["id"] = target_referenced_segment_id
        for val in current.values():
          if isinstance(val, (dict, list)):
            stack.append(val)
      elif isinstance(current, list):
        for item in current:
          if isinstance(item, (dict, list)):
            stack.append(item)

    return source_segment_json

  # Look up and inject "Existing Segment" rule segment references in target parent segment (by replacing referenced segment ids in segment's configuration)
  def replace_existing_segment_rules(source_segment_json, existing_segment_rules):
    for referenced_segment in existing_segment_rules:
      referenced_segment_json = get_segment_by_id(referenced_segment["id"])
      referenced_segment_name = referenced_segment_json["name"]
      referenced_segment_folder_path = build_source_folder_structure(get_folder_by_id(referenced_segment_json["segmentFolderId"]))
      target_segment_root_folder_id = next((item["id"] for item in get_target_master_segment_folders() if item["parentFolderId"] is None), None)
      # Folder path empty means that the referenced segment is in the parent segment's root folder
      if not referenced_segment_folder_path:
        target_referenced_segment_id = get_segment_id_in_folder(target_segment_root_folder_id, referenced_segment_name)
        # Found referenced segment in target parent segment's root folder
        if target_referenced_segment_id is not None:
          source_segment_json = replace_referenced_segment_id(referenced_segment["id"], target_referenced_segment_id, source_segment_json)
        # Not found, look up referenced segment by name in whole target parent segment
        else:
          print("Referenced segment not found. Aborting...")
          exit()
      # Folder path non-empty means we will need to traverse it, check if it's intact, and that the referenced segment exists in target
      else:
        referenced_segment_folder_path.reverse()
        i = 0
        for referenced_segment_folder in referenced_segment_folder_path:
          if i == 0:
            target_segment_folder_id = next((item["id"] for item in get_assets_in_folder(target_segment_root_folder_id)["data"] if item["attributes"].get("name") == referenced_segment_folder[0] and item["type"] == "folder-segment"), None)
            # Path does not exist, look up referenced segment by name in whole target parent segment
            if target_segment_folder_id is None:
              print("Referenced segment path not found. Aborting...")
              exit()
          else:
            target_segment_folder_id = next((item["id"] for item in get_assets_in_folder(target_segment_folder_id)["data"] if item["attributes"].get("name") == referenced_segment_folder[0] and item["type"] == "folder-segment"), None)
            # Path does not exist, look up referenced segment by name in whole target parent segment
            if target_segment_folder_id is None:
              print("Referenced segment path not found. Aborting...")
              exit()
          i += 1
          if i == len(referenced_segment_folder_path):
            break
        target_referenced_segment_id = get_segment_id_in_folder(target_segment_folder_id, referenced_segment_name)
        # Segment does not exist in path, look up referenced segment by name in whole target parent segment
        if target_referenced_segment_id is None:
          print("Referenced segment not found. Aborting...")
          exit()
        source_segment_json = replace_referenced_segment_id(referenced_segment["id"], target_referenced_segment_id, source_segment_json)

    return source_segment_json["rule"]

  # Build the source segment's folder path as a list of folder names (upward traversal)
  def build_source_folder_structure(source_folder_json):
    folder_path = []
    
    if source_folder_json["data"]["relationships"]["parentFolder"]["data"] is not None:
      folder_path.append([source_folder_json["data"]["attributes"]["name"], source_folder_json["data"]["attributes"]["description"], source_folder_json["data"]["id"]])
      parent_folder_json = get_source_parent_folder(source_folder_json)
      while parent_folder_json["data"]["relationships"]["parentFolder"]["data"] is not None:
        folder_path.append([parent_folder_json["data"]["attributes"]["name"], parent_folder_json["data"]["attributes"]["description"], parent_folder_json["data"]["id"]])
        parent_folder_json = get_source_parent_folder(parent_folder_json)

    return folder_path

  # Sync segment with activation
  def replicate(target_master_segment_folders_json, source_folder_json, source_segment_json):  
    target_master_segment_root_folder = next((item for item in target_master_segment_folders_json if item["parentFolderId"] is None), None)
    target_segment_folder_id = target_master_segment_root_folder["id"]
    source_folder_path = build_source_folder_structure(source_folder_json)
    # Check source segment is directly under the source master segment's root folder
    if not source_folder_path:
      post_target_segment(source_segment_json, target_segment_folder_id)
    else:
      # Traverse folder path
      source_folder_path.reverse()
      for source_folder_name, source_folder_desc, source_folder_id in source_folder_path:
        target_asset_list_json = get_assets_in_folder(target_segment_folder_id)
        target_segment_folder = next((item["id"] for item in target_asset_list_json["data"] if item["attributes"].get("name") == source_folder_name and item["type"] == "folder-segment"), None)
        # Check folder exist
        if target_segment_folder is None:
          target_segment_folder_id = post_target_folder(source_folder_name, source_folder_desc, target_segment_folder_id)
        else:
          target_segment_folder_id = target_segment_folder
      post_target_segment(source_segment_json, target_segment_folder_id)

  # Replicate segment to each target audience
  for ta_id in target_audience_ids:
    target_audience_id = ta_id
    replicate(get_target_master_segment_folders(), get_source_folder(get_source_segment()), get_source_segment())
  
  print("Fin")

# Main
if __name__ == "__main__":
  main()
