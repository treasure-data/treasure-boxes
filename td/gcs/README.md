# Workflow: td example (Result Output to Google Cloud Storage)

This example workflow ingests data using [Treasure Data's Writing Job Results into Google Cloud Storage](https://docs.treasuredata.com/articles/result-into-google-cloud-storage) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/c7d87640f437d41bd6c7efeeb2793223.png)

![](https://t.gyazo.com/teams/treasure-data/8a59641ff11cb32d97f9d7c2c785613b.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_gcs

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_gcs --set key=value

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key=value

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_gcs export_gcs --session now

## Local mode

    # Run
    $ td wf run export_gcs.dig

# Supplemental

Available parameters for `result_settings` are here.

- bucket: (string, required)
- path_prefix: Prefix of output paths (string, required)
- sequence_format: (string, default: ".%03d.%02d")
- format: (string(csv|tsv), default csv)
- compression: (string(None|gz|bzip2), default None)
- header_line: (boolean(true|false), default true)
- delimiter: (string(","|"\t"|"tab","|"), default ",")
- quote_policy: (string(ALL|MINIMAL|NONE))
- null_string: (string(""|"\N"|NULL|null), default "")
- newline: (string(CRLF|CR|LF), default CRLF)
- application_name: (string, Arbitrary client name associated with API requests)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-google-cloud-storage#use-from-cli)

# Next Step

If you have any questions, please contact support@treasuredata.com.
