# Treasure Data MQTT Broker

[Treasure Data MQTT broker](https://support.treasuredata.com/hc/en-us/articles/360034799633-Data-Ingestion-Using-the-Treasure-Data-MQTT-Broker-Experimental) allows you to ingest data through the [MQTT protocol](http://mqtt.org/). 

Notice that our broker only accepts `publish` operation against a topic `mqtt-ingest`, and you cannot subscribe the topic. Plus, the MQTT broker currently requires client to be connected over SSL with a pair of given client certificate and RSA private key.

> ***The MQTT broker is currently experimental. Contact your Treasure Data Customer Success representative for more information and enablement.***

## Overview

In the multiple programming languages, this Box shows its basic usage by sequentially inserting two records with one-second interval:

|id|name|age|comment|object|array|
|:---:|:---:|:---:|:---:|:---:|:---:|
|1|John Doe|25|hello, world|{'lang', 'xxx'}|['hello', 'world']|
|2|Jane Doe|23|good morning|{'lang', 'xxx'}|['good', 'morning']|

## Usage

First, edit [`config.sample.json`](./config.sample.json) and rename as `config.json`.

Once the MQTT broker is enabled for your account, you should have a dedicated client certificate `certfile` and RSA private key `keyfile` that respectively contain the specific heading and tailing line:

```
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
```

```
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
```

Next, run the sample code as described in:

- [Java](./java)
- [Python](./python)
- [Ruby](./ruby)

As you can see, the `content` part of JSON payload represents single record (i.e., row) stored in Treasure Data:

```json
{
	"headers": {
		"time": (UNIX timestamp),
		"auth": (Treasure Data API key),
		"target": (destination database.table)
	},
	"content": {
		"column_name_1": (value_1),
		"column_name_2": (value_2),
		...
	}
}
```

Eventually, the records will become available on your target Treasure Data table.
