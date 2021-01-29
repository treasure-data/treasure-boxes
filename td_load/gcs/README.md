# Workflow: td_load example (Google Cloud Storage)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Google Cloud Storage](https://docs.treasuredata.com/display/public/INT/Google+Cloud+Storage+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Setting+Workflow+Secrets+from+the+Command+Line) feature, so that you don't have to include your database credentials to your workflow files.

# How to Run for Local Mode

First, please set database credentials by `td wf secrets` command.

    # Set Secrets for local
    $ td wf secrets --local td_load_example --set gcp.json_key=@credentails.json

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/gcs.yml](config/gcs.yml)

Now, you can run the workflow and trigger the session manually.

    $ td wf start td_load_gcs daily_load --session now

# How to Run for Server Mode

First, please upload the workflow.

    # Upload
    $ td wf push td_load_gcs

Next, please set database credentials by `td wf secrets` command.

    # Set Secrets for Server
    $ td wf secrets --project td_load_gcs --set gcp.json_key=@credentails.json

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/gcs.yml](config/gcs.yml)

Finally, you can trigger the session manually.

    # Run
    $ td wf start td_load_gcs daily_load --session now

# Appendix

This workflow uses `${session_date}` in path_prefix.
You can check built-in variables on [here](https://docs.digdag.io/workflow_definition.html#using-variables).

# Next Step

If you have any questions, please contact to support@treasuredata.com.
