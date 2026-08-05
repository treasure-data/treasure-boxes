# Treasure Data HTTP ingest: C Example

## Usage

### C with libcurl

An C source code example with [libcurl](https://curl.haxx.se/libcurl/)

```
cc -lcurl curl.c
./a.out c360-ingest-api.treasuredata.com 1/123456789abcdefghijklmnopqrstuvwxyz database_name table_name '{"events":[{"name":"John"}]}'
```
