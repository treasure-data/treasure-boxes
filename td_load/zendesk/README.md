# Workflow: td_load Example (Zendesk)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Zendesk](https://docs.treasuredata.com/display/public/INT/Zendesk+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set zendesk.login_url
    $ td wf secrets --project td_load_example --set zendesk.username
    $ td wf secrets --project td_load_example --set zendesk.token

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

| Keys     | Description |
| -------- | ----------- |
| login_url | Login URL for Zendesk. |
| auth_method | Auth method. `basic`, `token` and `oauth` are available. |
| target | Zendesk source such as `tickets`, `users`, and etc. |
| columns | Schema Settings. |

Depending on `auth_method`, other required the following keys exist:

- If `basic` is set, `username` (email address) and `password` are required.
- If `token` is set, `username` (email address) and `token` value are required.
- If `oauth` is set, `access_token` is required.

# Next Step

If you have any questions, please contact support@treasure-data.com.
