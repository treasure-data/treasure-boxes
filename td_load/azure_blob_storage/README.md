# Workflow: td_load Example (Microsoft Azure Blob Storage)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Microsoft Azure Blob Storage](https://tddocs.atlassian.net/wiki/spaces/PD/pages/1081764/Microsoft+Azure+Blob+Storage+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://tddocs.atlassian.net/wiki/spaces/PD/pages/223379597/Setting+Workflow+Secrets+from+the+Command+Line) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Second, please set datasource credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_load_example --set azure_blob_storage.account_name
    $ td wf secrets --project td_load_example --set azure_blob_storage.account_key

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

# Next Step

If you have any questions, please contact support@treasure-data.com.
