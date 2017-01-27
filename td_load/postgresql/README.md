# Workflow: td_load example (PostgreSQL)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for PostgreSQL](https://docs.treasuredata.com/articles/data-connector-postgresql) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run

First, please set database credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set postgresql.host=xyz
    $ td wf secrets --project td_load_example --set postgresql.port=5432
    $ td wf secrets --project td_load_example --set postgresql.user=abcde
    $ td wf secrets --project td_load_example --set postgresql.password=fghijklmn

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
