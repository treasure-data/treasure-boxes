# Workflow: td_load example (MySQL)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for MySQL](https://docs.treasuredata.com/display/public/INT/MySQL+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run

First, please set database credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set mysql.host
    $ td wf secrets --project td_load_example --set mysql.port
    $ td wf secrets --project td_load_example --set mysql.user
    $ td wf secrets --project td_load_example --set mysql.password

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now

# Required Keys

| Keys     | Description |
| -------- | ----------- |
| host     | Host information for MySQL. |
| user     | User name. |
| database | Database name. |

When you set `user_custom_query` is true, `query` option is required.
When you set `user_custom_query` is false, `select` and `table` options are required.

# Next Step

If you have any questions, please contact support@treasure-data.com.
