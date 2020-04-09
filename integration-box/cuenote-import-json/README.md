# Cuenote FC Delivery Log Import

## Prerequisite

### Note
This Workflow is for Cuenote FC's JSON API.
If your contract with YMIRLINK is for XML API, use the [Workflow for XML API](https://github.com/treasure-data/treasure-boxes/tree/master/integration-box/cuenote-import).

### Cuenote

- You need to have a username and a password for Cuenote API.
- IP addresses used by [Treasure Data Custom Script](https://support.treasuredata.com/hc/en-us/articles/360033974194-IP-Addresses-used-by-Custom-Scripts) must be allowed by the whitelist.
- For more information about preparation, please contact a representative or a support of YMIRLINK.

### Treasure Data

- Create a database dedicated for Cuenote integration. (no need to create tables)
- Generate an TD API Key with master-key permission.

## Installation

### 1. Push the workflow

```shell script
td wf push cuenote_import
```

### 2. Set variables for connecting to TD

```shell script
td wf secrets --project cuenote_import --set td.apikey td.apiserver td.database
```

|variable|sample|description|
|:----|:----|:----|
|`td.apikey`|`000/1234567890abcde`|Treasure Data's API key with Master-Key permission|
|`td.apiserver`|`https://api.treasuredata.com`|An endpoint of Treasure Data API. Use your [regional endpoint](https://support.treasuredata.com/hc/en-us/articles/360001474288-Sites-and-Endpoints).|
|`td.database`|`cuenote`|A name of database dedicated for Cuenote integration.|

### 3. Set variables for Cuenote API

```shell script
td wf secrets --project cuenote_import --set cn.endpoint cn.user cn.password
```

|variable|sample|description|
|:----|:----|:----|
|`cn.endpoint`|`https://fc00000.cuenote.jp/fcapi/v2.3/`|An endpoint of Cuenote FC API.|
|`cn.user`|`cuenote_user_hoge`|A username|
|`cn.password`|`abc123XYZ789`|A password|

### 4. Run a workflow "cuenote_import_master"

Once you completed #1 ~ #3, run a workflow named "cuenote_import_master".
Then, go to #5 if you confirmed that the first execution of the workflow is success.

Check if you see errors:

- Are TD IP addresses added to the Cuenote's IP whitelist?
- Did you create a database "cuenote"?
- Both endpoint TD & Cuenote is correct?
- Also, credentials for TD and Cuenote is exactly same as provided?

## Basic logic

- A workflow `cuenote_import_master` retrieves all Job Info from Cuenote API. This contains a basic information about delivery settings.
- A workflow `cuenote_import_delivery_logs` downloads logs for delivery jobs within the last 14 days then refresh the log tables.