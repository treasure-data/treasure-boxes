# Workflow: td_load Example (SFDC)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Amazon S3](https://docs.treasuredata.com/articles/data-connector-s3) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run

First, please set database credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set s3.endpoint=s3-us-west-1.amazonaws.com
    $ td wf secrets --project td_load_example --set s3.access_key_id=xyzxyzxyzxyz
    $ td wf secrets --project td_load_example --set s3.secret_access_key=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- https://github.com/treasure-data/workflow-examples/blob/master/td_load/sfdc/config/daily_load.yml

Now, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
