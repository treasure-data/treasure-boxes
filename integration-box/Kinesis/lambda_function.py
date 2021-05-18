import base64, time, json, sys
import dateutil, dateutil.parser, datetime
import urllib3

td_database = '<YOUR_DATABASE_NAME>'
td_table = '<YOUR_TABLE_NAME>'
td_master_key = '<YOUR_WRITE_ONLY_API_KEY>'
td_endpoint = 'https://in.treasuredata.com/js/v3/event'
 
def upload_td(records):
    headers = {
        'Content-Type': 'application/json',
        'X-TD-Data-Type': 'k',
        'X-TD-Write-Key': td_master_key,
    }
    data = json.dumps({ '%s.%s' % (td_database, td_table): records }).encode("utf-8")
    http = urllib3.PoolManager()
    req = http.request('POST',url=td_endpoint, body=data, headers=headers)
 
    resp = json.loads(req.data.decode('utf-8'))
    print("Success: %s records" % len(resp))
 
def lambda_handler(event):
    records = []
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        # We also assume payload comes as JSON form
        # Depending on the payload format, change code below to extract exact content from JSON object
        payload = json.loads(base64.b64decode(record["Sns"]))
        if (not 'time'in payload):
            payload['time'] = int(time.time())
        elif isinstance(payload['time'], basestring = str):
            payload['time'] = int((dateutil.parser.parse(payload['time']).replace(tzinfo=dateutil.tz.tzutc()) - datetime.datetime.utcfromtimestamp(0).replace(tzinfo=dateutil.tz.tzutc())).total_seconds())
        records.append(payload)
    upload_td(records)
