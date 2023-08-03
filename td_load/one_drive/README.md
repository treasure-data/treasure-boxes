# Workflow: td_load Example (One Drive)

This example workflow ingests data in daily basis, using [OneDrive Import Integration](https://docs.treasuredata.com/display/public/INT/OneDrive+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

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
| client_id| Y | OAuth client_id. (stirng)|
| client_secret | Y | OAuth client_secret. (stirng)|
| refresh_token | Y | refresh_token uses to exchange for new access_token. (stirng)|

Or, you can specify authentication info using td_authentication_id option.([Reusing the existing Authentication](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2#AmazonS3ImportIntegrationv2-reuseAuthenticationReusingtheexistingAuthentication))

## Load Settings
| Keys | Required | Description |
| -------- | ----------- | ----------- |
| account_type | Y | OneDrive account plan. business or personal. (stirng) |
| is_shared_root | N | applicable for business accout_type only. When true,  imports files directly shared with you (different from shared folders) (boolean) | 
| domain_name | N | required when account_type = business. The hostname of onedrive. E.g. mydrive.sharepoint.com (string)|
| server_relative_path | N | required when account_type = business. The URL path relative to domain. E.g /personal/user1_mydrive_onmicrosoft_com(string). |
| folder_path | N | required when is_shared_root = false. (string) |
| last_modified_time | N | Only import files modified after the specified timestamp. Timezone is UTC. If this parameter is empty, imports all files. Timestamp format: yyyy-MM-dd'T'HH:mm:ss.SSSZ E.g. 2019-05-01T10:00:00.121Z (string) |
| name_match_pattern | N | Only import files that match the provided filename regex. (string) |
| retry_limit | N | A number of retries attempt when an error occurs before the system gives up. (Integer default = 7) |
| retry_initial_wait_millis | N | The time, in milliseconds, between the first and second attempt. (Integer, Default: 500 milliseconds) |
| max_retry_wait_millis | N | The time, in milliseconds, between the second and all subsequent attempts. (Integer, Default: 300000 ~ 5 minutes) | 
| connection_timeout_millis | N | The time, in milliseconds, HTTP connect timeout. (Integer, Default: 60000 ~ 1 minute) |
| read_timeout_millis | N | The time, in milliseconds, HTTP read timeout. (Long, Default: 300000 ~ 5 minutes).|
| min_task_size | N | When the import folder contains too many small files, it would cause degradation in import performance. Set this value to combine multiple files per task for performance gaining. E.g. 4000000 ~ 4MB. (Long) |

# Next Step

If you have any questions, please contact support@treasure-data.com.
