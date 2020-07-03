# Workflow: td_load example (Google BigQuery)
This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Google BigQuery](https://support.treasuredata.com/hc/en-us/articles/360001647267-Data-Connector-for-Google-BigQuery) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

# How to Run for Server Mode
First, please upload the workflow. `bigquery` is the project name.

    # Upload
    $ td wf push bigquery

Next, please set BigQuery credential(JSON keyfile) by `td wf secrets` command.

    # Set Secrets for Server
    $ td wf secrets --project bigquery --set bq.json_key=@credential.json

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

Finally, you can trigger the session manually.

    # Run
    $ td wf start bigquery daily_load --session now

# Appendix
This workflow uses ${session_time} and ${session_date_compact} in query of bg.yml. These are the built-in variables on [here](https://docs.digdag.io/workflow_definition.html#using-variables).

# Next Step
If you have any questions, please contact support@treasure-data.com.
