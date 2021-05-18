import base64, time, json, sys
import dateutil, dateutil.parser, datetime
import urllib3
td_database = 'my_db'
td_table = 'my_table'
td_master_key = '.....'
td_endpoint = 'https://in.treasuredata.com/js/v3/event'
 
def upload_td(records):
    #
    headers = {
        'Content-Type': 'application/json',
        'X-TD-Data-Type': 'k',
        'X-TD-Write-Key': td_master_key,
    }
    # urllib3 module is a powerful, sanity-friendly HTTP client for Python. 
    # It supports thread safety, connection pooling, client-side SSL/TLS verification, file uploads with multipart encoding
    data = json.dumps({ '%s.%s' % (td_database, td_table): records }).encode("utf-8")
    http = urllib3.PoolManager()
    req = http.request('POST',url=td_endpoint, body=data, headers=headers)

    #req = urllib.request.Request(td_endpoint, data, headers=headers)
    #r = urllib.request.urlopen(req, timeout=180)
    #r.read().decode("utf-8")

    resp = json.loads(req.data.decode('utf-8'))
    print("Success: %s records" % len(resp))
 
def lambda_handler(event):
    records = []
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        # We also assume payload comes as JSON form
        # payload = json.loads(base64.b64decode(record["Sns"]["Timestamp"]))
        s1 = json.dumps(record)
        payload = json.loads(s1)
        print(payload)
        #print(payload["Sans"]["Timestamp"])
        if (not 'time'in payload):
            payload['time'] = int(time.time())
        elif isinstance(payload['time'], basestring = str):
            payload['time'] = int((dateutil.parser.parse(payload['time']).replace(tzinfo=dateutil.tz.tzutc()) - datetime.datetime.utcfromtimestamp(0).replace(tzinfo=dateutil.tz.tzutc())).total_seconds())
        records.append(payload)
        print(records)
    upload_td(records)

def main():
    event = {
            "Records": [
                {"Sans":
                    {
                        "Timestamp": "2019-01-02T12:45:07.000Z",
                        "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r=="
                    }
                }
            ]
    }
    lambda_handler(event)
    pass

if __name__ == "__main__":
    main()
