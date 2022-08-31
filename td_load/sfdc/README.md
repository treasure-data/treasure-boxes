# Workflow: td_load Example (SFDC)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Salesforce](https://docs.treasuredata.com/display/public/INT/Salesforce+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set sfdc.username
    $ td wf secrets --project td_load_example --set sfdc.password
    $ td wf secrets --project td_load_example --set sfdc.client_id
    $ td wf secrets --project td_load_example --set sfdc.client_secret
    $ td wf secrets --project td_load_example --set sfdc.security_token
    $ td wf secrets --project td_load_example --set sfdc.login_url

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

| Keys     | Description |
| -------- | ----------- |
| username | User name for force.com REST API. |
| password | Password for Force.com REST API. |
| client_id | Client ID for your application. |
| client_secret | Client secret for your application. |
| login_url | Your Login URL for Salesforce. |
| target | Target objact name. |

# Next Step

If you have any questions, please contact support@treasure-data.com.
