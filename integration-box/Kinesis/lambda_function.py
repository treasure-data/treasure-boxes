import base64
import time
import json
import os
import random
import urllib.request

TD_DATABASE = os.environ.get("TD_DATABASE")
TD_TABLE = os.environ.get("TD_TABLE")
TD_API_KEY = os.environ.get("TD_API_KEY")
TD_ENDPOINT = os.environ.get("TD_ENDPOINT", "https://us01.records.in.treasuredata.com")
TD_RETRIES = int(os.environ.get("TD_RETRIES", "10"))


def publish(records, retry_count=0):
    headers = {
        "Content-Type": "application/vnd.treasuredata.v1+json",
        "Accept": "application/vnd.treasuredata.v1+json",
        "Authorization": f"TD1 {TD_API_KEY}",
    }
    request = urllib.request.Request(
        f"{TD_ENDPOINT}/{TD_DATABASE}/{TD_TABLE}",
        json.dumps({"events": records}).encode("utf-8"),
        headers,
    )
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            return
        if response.status in (400, 401, 403, 422):
            raise RuntimeError(f"unexpected response: {response.status}")
        retries = records if response.status != 206 else failures(response, records)
        time.sleep(1 + random.uniform(0, 1))
        if retry_count > TD_RETRIES:
            print(f"Failed to send {len(retries)} records after {retry_count} tries")
        else:
            publish(retries)


def failures(response, records):
    parsed = json.load(response)
    return [
        entry
        for receipt, entry in zip(parsed["receipts"], records)
        if not receipt["success"]
    ]


def transform(record):
    # Kinesis data is base64 encoded so decode here
    # We also assume payload comes as JSON form
    # Depending on the payload format, change code below to extract exact content from JSON object
    payload = json.loads(base64.b64decode(record["data"]))
    if "time" not in payload:
        payload["time"] = int(time.time())
    return payload


def lambda_handler(event, context):
    records = map(transform, event)
    publish(records)
