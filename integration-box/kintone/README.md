# Integration with kintone
[kintone](https://www.kintone.com/) is a cloud service from Cybozu that allows us to easily create systems for our own business even if we do not have any knowledge of system development. We can use kintone to intuitively create business apps, and share them within team.
This code enable us to GET/DELETE kintone records from TD and PUT/POST TD records to kintone.

# Installation

## Prerequisite
- Need Treasure Data API key which is Master Key permission.
- Get kintone developper license and org ID.

# Edit *.dig and kintone.yml
1. main.dig: Input our org ID
2. kintone.yml: Write your apps' IDs and corresponding API keys/columns for POST/PUT.
3. get_records.dig: Input app ID/TD API key/identifier field code/fields to GET/query to GET records from kintone.
4. delete_records.dig: Input app ID/TD API key/ids of records to delete from kintone.
5. post_records.dig: Write app ID/TD API key/query to select records from TD to POST to kintone.
6. put_records.dig: Write app ID/TD API key/query to select records from TD to PUT to kintone.


# Run
- Now you can use integrations between kintone and TD.

# Output
