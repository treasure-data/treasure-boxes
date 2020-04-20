# Workflow: td example (Result Output to Microsoft Azure Blob Storage)

This example workflow exports TD job results into Microsoft Azure Blob Storage, using [Treasure Data's Writing Job Results into Microsoft Azure Blob Storage](https://docs.treasuredata.com/articles/result-into-microsoft-azure-blob-storage) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/168a1b20e49fe96d478c96d2f8731711.png)

![](https://t.gyazo.com/teams/treasure-data/fb37cccfb2b2127e1e8e2d6c74720d08.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_azure_blob_storage

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_azure_blob_storage --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_azure_blob_storage td_azure_blob_storage --session now

## Local mode

    # Run
    $ td wf run td_azure_blob_storage.dig

# Supplemental

Available parameters for `result_settings` are here.

- container: (string, required)
- path_prefix: (string, required)
- file_ext: (string, required)
- format: (string(csv|tsv), default csv)
- compression: (string(None|gz), default None)
- header_line: (boolean, default true)
- delimiter: (string(","|"\t"|"|"), default ",")
- null_string: (string(""|"\N"|NULL|null), default "")
- new_line: (string(CRLF|CR|LF), default CRLF)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-microsoft-azure-blob-storage)

# Next Step

If you have any questions, please contact support@treasure-data.com.
