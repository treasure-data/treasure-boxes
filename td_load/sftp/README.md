# Workflow: td_load Example (SFTP)

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for SFTP](https://docs.treasuredata.com/display/public/INT/SFTP+Server+Import+Integration) with [td_load](https://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Workflows+and+Machine+Learning-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set SFTP credentials by `td wf secrets` command. We recommend you to use text file for setting secret_key_file. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_load_example --set sftp.host
    $ td wf secrets --project td_load_example --set sftp.port
    $ td wf secrets --project td_load_example --set sftp.user
    $ td wf secrets --project td_load_example --set sftp.secret_key_passphrase
    $ td wf secrets --project td_load_example --set sftp.secret_key_file=@secret_key_file.txt

    # Set Secrets on your local for testing
    $ td wf secrets --local --set sftp.host
    $ td wf secrets --local --set sftp.port
    $ td wf secrets --local --set sftp.user
    $ td wf secrets --local --set sftp.secret_key_passphrase
    $ td wf secrets --local --set sftp.secret_key_file=@secret_key_file.txt

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Required Keys

| Keys     | Description |
| -------- | ----------- |
| host | Host name. |
| port | Port number. |
| user | User name. |
| path_prefix | Prefix of output paths. |

# Next Step

If you have any questions, please contact support@treasure-data.com.
