# Workflow: td example (Result Output to FTP(S))

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into FTP(S)](https://docs.treasuredata.com/articles/result-into-ftp) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/ce6d63afb6917ee99d7a5fdace2b7ccd.png)

![](https://t.gyazo.com/teams/treasure-data/55071234c2d489b7bb1bdbb342a067e0.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_ftp

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_ftp --set key=value

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key=value

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_ftp td_ftp --session now
    
# Supplemental

Available parameters for `result_settings` are here.

- path_prefix: Prefix of output paths (string, required)
- format: (string(csv|tsv), default csv)
- sequence_format: (string, default: ".%03d.%02d")
- compression: (string(None|gz|bzip2), default None)
- header_line: (boolean(true|false), default true)
- delimiter: (string(","|"\t"|"tab"|"|"), default ",")
- null_string: (string(""|"\N"|NULL|null), default "")
- newline: (string(CRLF|CR|LF), default CRLF)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-ftp#usage-from-cli)

# Next Step

If you have any questions, please contact support@treasure-data.com.
