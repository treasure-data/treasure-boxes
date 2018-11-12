# Workflow: td_load Example (FTP(S))

This example workflow ingests data in daily basis, using [Treasure Data's Data Connector for FTP](https://docs.treasuredata.com/articles/data-connector-ftp) with [td_load](http://docs.digdag.io/operators.html#td-load-treasure-data-bulk-loading) operator.

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example

Second, please set FTP credentials by `td wf secrets` command. We recommend you to use text file for setting secret_key_file. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_load_example --set ftp.host
    $ td wf secrets --project td_load_example --set ftp.port
    $ td wf secrets --project td_load_example --set ftp.user
    $ td wf secrets --project td_load_example --set ftp.password

    # Set Secrets on your local for testing
    $ td wf secrets --local --set ftp.host
    $ td wf secrets --local --set ftp.port
    $ td wf secrets --local --set ftp.user
    $ td wf secrets --local --set ftp.password

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

For more input parameter details, please see [FTP file input plugin documentation](https://github.com/embulk/embulk-input-ftp#configuration).

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
