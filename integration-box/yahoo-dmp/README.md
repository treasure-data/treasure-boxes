# Objective
There are 2 ways to create targeting campaign on Yahoo! Display Network.
1. Direct targeting using userlist sent by TreasureData (hereinafter called `Direct Targeting`)
2. Targeting using userlist created by Yahoo! DMP as CustomSegment made from userlist sent by TreasureData (hereinafter called `CustomSegment Targeting`)

# Requirement 
- Require to have accounts for TreasureData, Yahoo Display Network, Yahoo! DMP
- Require to have clientId(referred to `_a`), DatasourceNo(referred to `_b`) provided by Yahoo!
- Require to have vendor_guid, entity_id, uid_key, and x-api-key provided by TreasureData support team.
- Set up Treasure Data Toolbelt: Command-line Interface (https://support.treasuredata.com/hc/en-us/articles/360000720048-Treasure-Data-Toolbelt-Command-line-Interface) 

# Installation (Setup)  
Download this workflow. 

## define workflow 
### 1. Prepare SQL query
To extract userIds, write down a sql query.
Direct Targeting must requires just only 1 column result. CustomSegment Targeting must requires multipul columns.(userId, attribute1, attribute2, attribute3.....)

example 1) `queries/userlist.sql` for Direct Targeting.
example 2) `queries/userlist_with_attr.sql` for CustomSegment Targeting.

Once you wrote sql, replace setting to refer to it.
```
  sqlfile      : queries/userlist.sql
```
### 2. Set database name on _export.
```
_export:
  td:
    database: ******
```
### 3. Specify fixed string for tag_definition_guid
For Direct Targeting
```
tag_definition_guid : yahoo_japan_ydn_custom_audience_server
```

For CustomSegment Targeting
```
tag_definition_guid : yahoo_japan_dmp_fuse
```


### 4. Set Yahoo DMP API information
information are provided by TreasureData support team.
- vendor_guid
- entity_id
- uid_key

### 4. Set Yahoo DMP information you want to send to.
- brand_guid

    You can pick `brand_guid` on Yahoo! DMP web console.

- tag_fields

    For Direct Targeting
    ```
      tag_fields:
          p: ******
          lid: ******
    ```

    CustomSegment Targeting
    ```
      tag_fields          :
        _a: ******
        _d: ******
        vars:
          type  : 1
          price : 2
    ```
    `_a` is a clientId for Yahoo! DMP, `_b` is a DatasourceNo for Yahoo! DMP. Both values are provided by Yahoo. (Please contact Yahoo representative)
    As for `vars` value, you have to set combinations of a column name and column number.
    Assuming that your sql result is following, you should set type: 1 and price: 2.
    ```
    userId, type    , price
    0001  , Android , 100
    0002  , Android , 200
    0003  , iOS     , 150
    ```


### push to TreasureData as Workflow project  
Push it to your TD environment, 
``` 
$ td wf push yahoodmp_integration  
``` 

### set secrets
- Set `x_api_key` as Secrets.
- Set `td.apikey` as Secrets.

FYI
Setting Workflow Secrets from TD Console
https://tddocs.atlassian.net/wiki/spaces/PD/pages/219185771/Setting+Workflow+Secrets+from+TD+Console

# Mechanism 
<img width="2999" alt="yahoodmp_integration" src="https://user-images.githubusercontent.com/248312/82309034-8d065700-99fd-11ea-8066-96923cf397b5.png">
