# Workflow: td_load Example (NetSuite)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for NetSuite](https://docs.treasuredata.com/articles/data-connector-netsuite) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set netsuite.email=xyzxyz
    $ td wf secrets --project td_load_example --set netsuite.password=xyzxyz
    $ td wf secrets --project td_load_example --set netsuite.account=xyzxyz
    $ td wf secrets --project td_load_example --set netsuite.role=xyzxyz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
