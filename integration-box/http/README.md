# Treasure Data Streaming Ingest API

Treasure Data Streaming Ingest API allows you to ingest data through HTTPS.

## Overview

In the multiple programming languages, this Box shows its basic usage by sequentially inserting two records:

|id|name|age|comment|object|array|
|:---:|:---:|:---:|:---:|:---:|:---:|
|1|John Doe|25|hello, world|{'lang', 'xxx'}|['hello', 'world']|
|2|Jane Doe|23|good morning|{'lang', 'xxx'}|['good', 'morning']|

## Usage

First, edit [`config.sample.json`](./config.sample.json) and rename as `config.json`.

As you can see, the `events` part of JSON payload represents single record (i.e., row) stored in Treasure Data:

```json
{
	"events": [{
		"column_name_1": (value_1),
		"column_name_2": (value_2),
		...
	}, ...]
}
```

Eventually, the records will become available on your target Treasure Data table.
