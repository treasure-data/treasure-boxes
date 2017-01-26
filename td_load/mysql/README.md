# Workflow: td_load_example

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for MySQL](https://docs.treasuredata.com/articles/data-connector-mysql) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run

First, please set database credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set mysql.host=xyz
    $ td wf secrets --project td_load_example --set mysql.port=3306
    $ td wf secrets --project td_load_example --set mysql.user=abcde
    $ td wf secrets --project td_load_example --set mysql.password=fghijklmn

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- https://github.com/treasure-data/workflow-examples/blob/master/td_load_example/config/daily_replace.yml

Now, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_laod_example daily_replace --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
