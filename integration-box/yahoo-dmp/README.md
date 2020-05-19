# Requirement 
set up Treasure Data Toolbelt: Command-line Interface (https://support.treasuredata.com/hc/en-us/articles/360000720048-Treasure-Data-Toolbelt-Command-line-Interface) 

# Installation (Setup)  
Download this workflow. 

### define workflow 
1. Prepare SQL query to extract userIds and write it down `queries/userlist.sql`.
2. Set database name on _export.
3. Set Yahoo DMP API information provided by TreasureData support team.
  - vendor_guid
  - entity_id
  - uid_key
4. Set Yahoo DMP information you want to send to.
  - brand_guid
  - tag_fields_p
  - tag_fields_lid



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
