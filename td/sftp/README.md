# Workflow: td example (Result Output to SFTP)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into SFTP](https://docs.treasuredata.com/articles/result-into-sftp) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/fc51459feff2d086df97f5f7eb8f6f72.png)

![](https://t.gyazo.com/teams/treasure-data/43dec12525f6cd0ee5ba7240bbc08892.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_sftp

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sftp --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_sftp td_sftp --session now

## Local mode

    # Run
    $ td wf run td_sftp.dig

# Supplemental

Available parameters for `result_settings` are here.

- user_directory_is_root: (boolean(true|false), default true)
- path_prefix: Prefix of output paths (string, required)
- format: (string(csv|tsv), default csv)
- compression: (string(None|gz|bzip2), default None)
- header_line: (boolean(true|false), default true)
- delimiter: (string(","|"\t"), default ",")
- quote_policy: (string(ALL|MINIMAL|NONE))
- null_string: (string(""|"\N"|NULL|null), default "")
- newline: (string(CRLF|CR|LF), default CRLF)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-sftp#usage-from-cli)

# Next Step

If you have any questions, please contact support@treasure-data.com.
