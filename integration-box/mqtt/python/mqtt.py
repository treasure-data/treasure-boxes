import json
import paho.mqtt.client as mqtt
from pathlib import Path
import ssl
import time


def on_log(client, userdata, level, buf):
    print('log: {}'.format(buf))


def on_disconnect(client, userdata, rc):
    client.loop_stop()


with Path(__file__).absolute().parent.parent.joinpath('config.json').open() as f:
    config = json.load(f)

account_id = config['apikey'].split('/')[0]

client = mqtt.Client()
client.on_log = on_log
client.on_disconnect = on_disconnect
client.tls_set(certfile=config['certfile'],
               keyfile=config['keyfile'],
               cert_reqs=ssl.CERT_NONE,
               tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set(account_id, password=config['apikey'])

client.connect(config['broker'], 8883)
client.loop_start()

target = '{}:{}'.format(config['database'], config['table'])
topic = 'mqtt-ingest'
qos = 1

payload = {
    'headers': {
        'time': int(time.time()),
        'auth': config['apikey'],
        'target': target
    },
    'content': {
        'id': 1,
        'name': 'John Doe',
        'age': 25,
        'comment': 'hello, world',
        'object': {'lang': 'python'},
        'array': ['hello', 'world']
    }
}
client.publish(topic, json.dumps(payload), qos)

time.sleep(1)

payload = {
    'headers': {
        'time': int(time.time()),
        'auth': config['apikey'],
        'target': target
    },
    'content': {
        'id': 2,
        'name': 'Jane Doe',
        'age': 23,
        'comment': 'good morning',
        'object': {'lang': 'python'},
        'array': ['good', 'morning']
    }
}
client.publish(topic, json.dumps(payload), qos)

time.sleep(1)

client.disconnect()
