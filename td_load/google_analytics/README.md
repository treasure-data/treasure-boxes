# Workflow: td_load Example (Google Analytics)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for Google Analytics](https://docs.treasuredata.com/articles/data-connector-google-analytics) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set Google Analytics credentials by `td wf secrets` command with text file. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_load_example --set json_key_content=@secrets.txt

    # Set Secrets on your local for testing
    $ td wf secrets --local --set json_key_content=@secrets.txt

## Configuration (v0.9.21 or earlier)

NOTE: Latest version fixes this issue.

`private_key` part in `json_key_content` has to care Line Feed Code using escape key.

    # private_key in secret_key_file format for secret
    "private_key": "-----BEGIN PRIVATE KEY-----\\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\nBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\\nCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\\nDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD\\nuEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE\\nZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\\n-----END PRIVATE KEY-----\\n",

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
