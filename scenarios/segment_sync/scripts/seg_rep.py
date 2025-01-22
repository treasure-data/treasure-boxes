import os
import requests

def main(**kwargs):
  # Init
  td_api_key = os.getenv("TD_API_KEY")
  aud_api_ep = kwargs.get("aud_api_ep")
  audience = str(kwargs.get("audience"))
  batch_folder = str(kwargs.get("batch_folder"))
  rt_folder = str(kwargs.get("rt_folder"))
  get_seg_list_path = kwargs.get("get_seg_list_path")
  post_new_seg_path = kwargs.get("post_new_seg_path")
  mode = kwargs.get("mode")
  get_b_seg_list_path = aud_api_ep + get_seg_list_path.replace("{audienceId}", audience).replace("{folderId}", batch_folder)
  get_rt_seg_list_path = aud_api_ep + get_seg_list_path.replace("{audienceId}", audience).replace("{folderId}", rt_folder)
  post_new_seg_path = aud_api_ep + post_new_seg_path.replace("{audienceId}", audience)
  b_data_dict = {}
  b_name_set = set()
  rt_data_dict = {}
  rt_name_set = set()

  # Get segments data via Audience API
  def get_segs():
    payload = {}
    headers = {
      "Authorization": f"TD1 {td_api_key}"
    }
    batch_segs = requests.request("GET", get_b_seg_list_path, headers = headers, data = payload)
    rt_segs = requests.request("GET", get_rt_seg_list_path, headers = headers, data = payload)

    if batch_segs.status_code == 200 and rt_segs.status_code == 200:
      batch_segs_list = batch_segs.json()
      rt_segs_list = rt_segs.json()
    elif batch_segs != 200 and rt_segs.status_code != 200:
      print(f"Failed to fetch batch segments. Status code: {batch_segs.status_code} - {batch_segs.reason} - {batch_segs.text}")
      print(f"Failed to fetch real-time segments. Status code: {rt_segs.status_code} - {rt_segs.reason} - {rt_segs.text}")
      exit()
    elif batch_segs == 200 and rt_segs.status_code != 200:
      print(f"Failed to fetch real-time segments. Status code: {rt_segs.status_code} - {rt_segs.reason} - {rt_segs.text}")
      exit()
    elif batch_segs != 200 and rt_segs.status_code == 200:
      print(f"Failed to fetch batch segments. Status code: {rt_segs.status_code} - {rt_segs.reason} - {rt_segs.text}")
      exit()
    else:
      print("Unknown error.")
      exit()

    return batch_segs_list, rt_segs_list

  # Build segment lists
  def build_seg_lists():
    for i in range(len(batch_segs_list)):
      b_data_dict[batch_segs_list[i]["name"]] = [batch_segs_list[i]["id"], batch_segs_list[i]["description"], batch_segs_list[i]["rule"]]
      b_name_set.add(batch_segs_list[i]["name"])
    for j in range(len(rt_segs_list)):
      rt_data_dict[rt_segs_list[j]["name"]] = [rt_segs_list[j]["id"], rt_segs_list[j]["description"], rt_segs_list[j]["rule"]]
      rt_name_set.add(rt_segs_list[j]["name"])

  # Post new segment via Audience API
  def post_seg(seg_name, headers, payload):
    new_seg = requests.request("POST", post_new_seg_path, headers = headers, json = payload)
    if new_seg.status_code == 200:
      print(f"Segment synced OK: '{seg_name}'")
    else:
      print(f"Failed to post segment: '{seg_name}' - Status code: {new_seg.status_code} - {new_seg.reason} - {new_seg.text}")

  # Segments that have time within past operator or segment reference
  def detect_unconvertible(sn, rule):
    twp = False
    seg_ref = False
    for c in rule.get("conditions", []):
      if "conditions" in c:
        for sc in c["conditions"]:
          if str(sc).find("'type': 'TimeWithinPast'") > 0:
            print(f"TWP operator found in '{sn}'.")
            twp = True
          if str(sc).find("'type': 'Reference'") > 0:
            print(f"Segment reference found in '{sn}'.")
            seg_ref = True
    return twp or seg_ref

  # Segments that already exist by segment name
  def detect_existing(sn, ns2):
    seg_exists = False
    if sn in ns2:
      print(f"Segment '{sn}' already exists.")
      seg_exists = True
    return seg_exists

  # Compare segment lists and create diff
  def replicate_diff():
    if mode == 0:
      folder = rt_folder
      kind = 1
      name_set1 = b_name_set
      name_set2 = rt_name_set
      data_dict = b_data_dict
    elif mode == 1:
      folder = batch_folder
      kind = 0
      name_set1 = rt_name_set
      name_set2 = b_name_set
      data_dict = rt_data_dict
    else:
      print("Configuration error.")
      exit()
    for sn in name_set1:
      if not detect_existing(sn, name_set2) and not detect_unconvertible(sn, data_dict[sn][2]):
        payload = {
          'audienceId': audience,
          'name': sn,
          'kind': kind,
          'description': data_dict[sn][1] + ' --- [Created from: ' + data_dict[sn][0] + ' ]',
          'segmentFolderId': folder,
          'rule': data_dict[sn][2]
        }
        headers = {
          "Authorization": f"TD1 {td_api_key}",
          "Content-Type": "application/json"
        }
        post_seg(sn, headers, payload)

  batch_segs_list, rt_segs_list = get_segs()
  build_seg_lists()
  replicate_diff()
        
  #Stats
  print("Batch segment count (before): " + str(len(batch_segs_list)))
  print("Real-time segment count (before): " + str(len(rt_segs_list)))
  batch_segs_list, rt_segs_list = get_segs()
  print("Batch segment count (after): " + str(len(batch_segs_list)))
  print("Real-time segment count (after): " + str(len(rt_segs_list)))

  print("Fin")

# Main
if __name__ == "__main__":
  main()
