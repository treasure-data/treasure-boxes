# Workflow: td_load Example (Marketo)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Marketo](https://docs.treasuredata.com/articles/data-connector-marketo) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set marketo.account_id
    $ td wf secrets --project td_load_example --set marketo.client_id
    $ td wf secrets --project td_load_example --set marketo.client_secret

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load_activity_log.yml](config/daily_load_activity_log.yml)
- [config/daily_load_lead.yml](config/daily_load_lead.yml)

If you use Treasure Workflow UI, overwrite above parameters into ${secret:marketo.xxxx} in yml files directly.

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

Before you trigger, confirm whether there is a target database and tables.
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
