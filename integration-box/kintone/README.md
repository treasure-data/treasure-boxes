# Integration with kintone
[kintone](https://www.kintone.com/) is a cloud service from Cybozu that allows us to easily create systems for our own business even if we do not have any knowledge of system development. We can use kintone to intuitively create business apps, and share them within team.
This code enable us to GET/DELETE kintone records from TD and PUT/POST TD records to kintone.

# Installation

## Prerequisite
- Need Treasure Data API key which is Master Key permission.
- Get kintone developper license and org ID.

## Push the code and set variables
```sh
td wf push kintone
td wf secrets --project kintone --set td.apikey td.endpoint
```

|Variable|Description|Example|
|:---|:---|:---|
|`td.apikey`|An API key to be used in the script. Access Type must be `Master Key`.|`1234/abcdefghijklmnopqrstuvwxyz1234567890`|
|`td.endpoint`|TD's API endpoint starting with `https://`.|`https://api.treasuredata.com`|


# Edit *.dig and kintone.yml

1. main.dig: Input our org ID
2. kintone.yml: Write your apps' IDs and corresponding API keys and column names for POST/PUT.
3. get_records.dig: Input app ID and identifier field code and fields to GET and query to GET records from kintone.
4. delete_records.dig: Input ids of records to delete and app ID.
5. post_records.dig: Write query to select records from TD to POST to kintone.
6. put_records.dig: Write query to select records from TD to POST to kintone.


# Run
