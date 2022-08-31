# Workflow: td_load Example (Salesforce Marketing Cloud)

This example workflow ingests data in daily basis incrementally and fetches data from yesterday for 1 day, using [Treasure Data's Data Connector for SFMC](https://docs.treasuredata.com/display/public/INT/Salesforce+Import+Integration-marketing-cloud) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

## For local mode testing

First, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --local --set sfmc.client_id
    $ td wf secrets --local --set sfmc.client_secret

    # Run
    $ td wf run daily_load.dig

## To upload to workflow server 

You can upload the workflow.

    # Upload
    $ td wf push td_load_example

Please set datasource credentials by `td wf secrets` command for the project

    # Set Secrets
    $ td wf secrets --project td_load_example --set sfmc.client_id
    $ td wf secrets --project td_load_example --set sfmc.client_secret


Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

| Keys     | Description |
| -------- | ----------- |
| client_id | Client ID for SFMC. |
| client_secret | Client secret for SFMC. |
| auth_uri | Authentication url. |
| de_name | Data Extention name. |

If you use SFMC enhanced package ([SFMC v2 integration](https://docs.treasuredata.com/display/public/INT/Salesforce+Marketing+Cloud+Import+Integration+CLI+v2)), set `auth_type: v2`, which option is `v1` to default.

# Next Step

If you have any questions, please contact support@treasure-data.com.
