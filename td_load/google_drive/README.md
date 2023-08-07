# Workflow: td_load Example (Google Drive)

This example workflow ingests data in daily basis, using [Google Drive Import Integration](https://docs.treasuredata.com/display/public/INT/Google+Drive+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required/Optional Keys
## Authentication
| Keys     | Required | Description |
| -------- | ----------- | ----------- |
| client_id | Y | OAuth client_id. (stirng)|
| client_secret | Y | OAuth client_secret. (stirng)|
| refresh_token | Y | OAuth refresh_token uses to exchange access_token. (stirng)|

Or, you can specify authentication info using td_authentication_id option.([Reusing the existing Authentication](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2#AmazonS3ImportIntegrationv2-reuseAuthenticationReusingtheexistingAuthentication))

## Load Settings
| Keys | Required | Description |
| -------- | ----------- | ----------- |
| target | N | Import from Folder or File , enum: "folder", "file". (stirng, default: "folder") |
| id | Y | Google Drive Folder ID or File ID. (string)|
| filename_pattern | N | Only import files that have filename match with regex.(string)|
| last_modified_time | N | Only import files modified after this timestamp. Timezone is UTC. If this parameter is empty, import all files. (string) |
| maximum_retries | N | Max retry count. (integer, default: 7)|
| initial_retry_interval_millis | N | Initial retry interval by milli seconds.(integer, default: 1000) |
| maximum_retry_interval_millis	| N | Max retry interval by milli seconds.(integer, default: 120000)|

# Next Step

If you have any questions, please contact support@treasure-data.com.
