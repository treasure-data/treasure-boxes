# Workflow: td_load Example (SFDC)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Salesforce](https://docs.treasuredata.com/articles/data-connector-salesforce) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run

First, please set database credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set sfdc.username=xyz
    $ td wf secrets --project td_load_example --set sfdc.password=xyz
    $ td wf secrets --project td_load_example --set sfdc.client_id=xyz
    $ td wf secrets --project td_load_example --set sfdc.client_secret=xyz
    $ td wf secrets --project td_load_example --set sfdc.security_token=xyz
    $ td wf secrets --project td_load_example --set sfdc.login_url=http://xyz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- https://github.com/treasure-data/workflow-examples/blob/master/td_load/sfdc/config/daily_load.yml

Now, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
