# Workflow: td_load Example (Facebook Leads)

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
| access_token | Y | Facebook long-lived access token (string, required) |
| app_secret | Y | client app_secret (string)|

Or, you can specify authentication info using td_authentication_id option.([Reusing the existing Authentication](https://docs.treasuredata.com/display/public/INT/Amazon+S3+Import+Integration+v2#AmazonS3ImportIntegrationv2-reuseAuthenticationReusingtheexistingAuthentication))

## Load Settings
| Keys | Required | Description |
| -------- | ----------- | ----------- |
| ad_account_id | N | Facebook Ad Account ID. Leave blank to retrieve by each form/ads. (string) |
| id | N | Form ID/Ad ID. This parameter will override the ad account ID. Leave blank to retrieve by ad account. (string) |
| time_created | N | import Leads data submitted since this time until the current time. The field accepts ISO 8601 date-time format. E.g. 2020-01-01T00:00:00+0700 (string) |
| enable_guess_schema | N | If enabled, use the first data received to guess schema. Data might be missed if the form fields are inconsistent and not found in the guess schema. |
| form_fields | N | Required when enable_guess_schema=false Facebook Lead Form fields name and its data type.  (array, see the following details) | 
| skip_invalid_records | N | If selected will skip invalid Leads data and continue to import others, otherwise will fail job if encounter an invalid data. (boolean, default: false) | 
| columns | N | import data settings. (array, see the following details) |
| retry_limit | N | Maximum Retry Limit. (int, default: 7) |
| initial_retry_wait | N | Initial Retry Wait (Seconds). (int, default: 2) |
| max_retry_wait | N | Maximum Retry Wait (Seconds). (int, default: 240) |
| connection_timeout | N | HTTP Connection Timeout (Seconds). (int, default: 300)|
| read_timeout | N | HTTP Read Timeout (Seconds). (int, default: 120)|

Each element of form_fields and columns options have the following options.

| key | Required | Descritpion |
| -------- | ----------- | ----------- |
| name | Y | Form field name. |
| type | Y | Field data type. |
| format | N | Timestamp format. E.g. %Y-%m-%dT%H:%M:%S%z |


# Next Step

If you have any questions, please contact support@treasure-data.com.
