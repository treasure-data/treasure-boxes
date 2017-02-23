# Workflow: td example (Result Output to Microsoft Azure Blob Storage)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into Microsoft Azure Blob Storage](https://docs.treasuredata.com/articles/result-into-microsoft-azure-blob-storage) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by td wf push command.

    # Upload
    $ td wf push sample_project

Second, please set Microsoft Azure credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project sample_project --set azure.account_name=xyzxyzxyzxyz
    $ td wf secrets --project sample_project --set azure.account_key=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set azure.account_name=xyzxyzxyzxyz
    $ td wf secrets --local --set azure.account_key=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_microsoft_azure_blob_storage --session now
    
# Supplemental

JSON format of Result Output to Microsoft Azure Blob Storage is the following.

- {"type":"azure_blob_storage","account_name":"xxxx","account_key":"xxxx","container":"xxxx","path_prefix":"/path/to/file","file_ext":".csv","sequence_format":"","header_line":true,"quote_policy":"MINIMAL","delimiter":",","null_string":"","newline":"CRLF"}

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-microsoft-azure-blob-storage)

# Next Step

If you have any questions, please contact support@treasure-data.com.
