# Workflow: td example (Result Output to Salesforce Marketing Cloud (ExactTarget))

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into Salesforce Marketing Cloud (ExactTarget)](https://docs.treasuredata.com/articles/result-into-salesforce-marketing-cloud) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/6e1b959a45fcca59a72466bb4984e047.png)

![](https://t.gyazo.com/teams/treasure-data/baf128c600fac7c65394a7537f863720.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_sfmc

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sfmc --set key=value

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key=value

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_sfmc td_sfmc --session now

## Local mode

    # Run
    $ td wf run td_sfmc.dig

# Supplemental

Available parameters for `result_settings` are here.

- path_prefix: Prefix of output paths (string, required)
- format: (string(csv|tsv), default csv)
- compression: (string(None|gz|bzip2), default None)
- header_line: (boolean(true|false), default true)
- delimiter: (string(","|"\t"|"tab"), default ",")
- quote_policy: (string(ALL|MINIMAL|NONE))
- null_string: (string(""|"\N"|NULL|null), default "")
- newline: (string(CRLF|CR|LF), default CRLF)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-salesforce-marketing-cloud#run-a-treasure-data-job-to-complete-an-initial-import-to-salesforce)

# Next Step

If you have any questions, please contact support@treasure-data.com.
