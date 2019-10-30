require 'json'
require 'mqtt'

config = File.open(File.expand_path('../config.json', __dir__)) { |f|
  JSON.parse(f.read)
}

account_id = config['apikey'].split('/').first

client = MQTT::Client.new(config['broker'], :ssl => :TLSv1_2)
client.cert = File.read(config['certfile'])
client.key = File.read(config['keyfile'])
client.username = account_id
client.password = config['apikey']

client.connect('td-mqtt-sample')

target = "#{config['database']}:#{config['table']}"
topic = 'mqtt-ingest'
qos = 1

payload = {
    headers: {
      time: Time.now.to_i,
      auth: config['apikey'],
      target: target,
    },
    content: {
      id: 1,
      name: 'John Doe',
      age: 25,
      comment: 'hello, world',
      object: {lang: 'ruby'},
      array: %w[hello world]
    }
}
client.publish(topic, JSON.dump(payload), false, qos)

sleep 1

payload = {
    headers: {
      time: Time.now.to_i,
      auth: config['apikey'],
      target: target,
    },
    content: {
      id: 2,
      name: 'Jane Done',
      age: 23,
      comment: 'good morning',
      object: {lang: 'ruby'},
      array: %w[good morning]
    }
}
client.publish(topic, JSON.dump(payload), false, qos)

sleep 1

client.disconnect
