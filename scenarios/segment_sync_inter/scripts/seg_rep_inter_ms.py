import os
import requests

def main(**kwargs):
  # Init
  td_api_key = os.getenv("TD_API_KEY")
  aud_api_ep = kwargs.get("aud_api_ep")
  from_audience = str(kwargs.get("from_audience"))
  to_audience = str(kwargs.get("to_audience"))
  from_folder = str(kwargs.get("from_folder"))
  to_folder = str(kwargs.get("to_folder"))
  get_seg_list_path = kwargs.get("get_seg_list_path")
  post_new_seg_path = kwargs.get("post_new_seg_path")
  get_from_seg_list_path = aud_api_ep + get_seg_list_path.replace("{audienceId}", from_audience).replace("{folderId}", from_folder)
  get_to_seg_list_path = aud_api_ep + get_seg_list_path.replace("{audienceId}", to_audience).replace("{folderId}", to_folder)
  post_new_seg_path = aud_api_ep + post_new_seg_path.replace("{audienceId}", to_audience)
  from_data_dict = {}
  from_name_set = set()
  to_data_dict = {}
  to_name_set = set()

  # Get segments data via Audience API
  def get_segs():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    from_segs = requests.request("GET", get_from_seg_list_path, headers = headers, data = payload)
    to_segs = requests.request("GET", get_to_seg_list_path, headers = headers, data = payload)

    if from_segs.status_code == 200 and to_segs.status_code == 200:
      from_segs_list = from_segs.json()
      to_segs_list = to_segs.json()
    elif from_segs.status_code != 200 and to_segs.status_code != 200:
      print(f"Failed to fetch from segments. Status code: {from_segs.status_code} - {from_segs.reason} - {from_segs.text}")
      print(f"Failed to fetch to segments. Status code: {to_segs.status_code} - {to_segs.reason} - {to_segs.text}")
      exit()
    elif from_segs.status_code == 200 and to_segs.status_code != 200:
      print(f"Failed to fetch to segments. Status code: {to_segs.status_code} - {to_segs.reason} - {to_segs.text}")
      exit()
    elif from_segs.status_code != 200 and to_segs.status_code == 200:
      print(f"Failed to fetch from segments. Status code: {from_segs.status_code} - {from_segs.reason} - {from_segs.text}")
      exit()
    else:
      print("Unknown error.")
      exit()

    return from_segs_list, to_segs_list

  # Build segment lists
  def build_seg_lists():
    for i in range(len(from_segs_list)):
      from_data_dict[from_segs_list[i]["name"]] = [from_segs_list[i]["id"], from_segs_list[i]["description"], from_segs_list[i]["rule"], from_segs_list[i]["kind"]]
      from_name_set.add(from_segs_list[i]["name"])
    for j in range(len(to_segs_list)):
      #to_data_dict[to_segs_list[j]["name"]]
      to_name_set.add(to_segs_list[j]["name"])

  # Post new segment via Audience API
  def post_seg(seg_name, headers, payload):
    new_seg = requests.request("POST", post_new_seg_path, headers = headers, json = payload)
    if new_seg.status_code == 200:
      print(f"Segment synced OK: '{seg_name}'")
    else:
      print(f"Failed to post segment: '{seg_name}' - Status code: {new_seg.status_code} - {new_seg.reason} - {new_seg.text}")

  # Segments that already exist by segment name
  def detect_existing(sn, ns2):
    seg_exists = False
    if sn in ns2:
      print(f"Segment '{sn}' already exists.")
      seg_exists = True
    return seg_exists

  # Segments that have existing segment reference
  def detect_seg_ref(sn, rule):
    seg_ref = False
    for c in rule.get("conditions", []):
      if "conditions" in c:
        for sc in c["conditions"]:
          if str(sc).find("'type': 'Reference'") > 0:
            seg_ref = True
    return seg_ref
  
  # Extract existing segments from segment rule
  def extract_existing_segments(rule):
    ref_list = []
    for condition_group in rule["conditions"]:
      for condition in condition_group.get("conditions", []):
        if condition.get("type") == "Reference" and "id" in condition:
            ref_list.append(condition["id"])
    return ref_list

  # Compare segment lists and create diff
  def replicate_diff():
    for sn in from_name_set:
      rule = from_data_dict[sn][2]
      kind = from_data_dict[sn][3]
      desc = from_data_dict[sn][1]
      if not detect_existing(sn, to_name_set) and not detect_seg_ref(sn, rule):
        payload = {
          'audienceId': to_audience,
          'name': sn,
          'kind': kind,
          'description': desc,
          'segmentFolderId': to_folder,
          'rule': rule
        }
        headers = {
          "Authorization": f"TD1 {td_api_key}",
          "Content-Type": "application/json"
        }
        post_seg(sn, headers, payload)
      elif detect_seg_ref(sn, rule):
        ref_seg_ids = extract_existing_segments(rule)
        print(f"Skipping '{sn}'. Found referenced segment ids: '{ref_seg_ids}'.")

  from_segs_list, to_segs_list = get_segs()
  build_seg_lists()
  replicate_diff()
        
  #Stats
  print("Source segment count (before): " + str(len(from_segs_list)))
  print("Destination segment count (before): " + str(len(to_segs_list)))
  from_segs_list, to_segs_list = get_segs()
  print("Source segment count (after): " + str(len(from_segs_list)))
  print("Destination segment count (after): " + str(len(to_segs_list)))

  print("Fin")

# Main
if __name__ == "__main__":
  main()
