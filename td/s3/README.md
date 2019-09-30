# Workflow: td example (Result Output to s3)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into AWS S3](https://docs.treasuredata.com/articles/result-into-s3) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/0a42f334d6f7077999cf3b3abd868548.png)

![](https://t.gyazo.com/teams/treasure-data/4b85a78fe25665f1d417b469e7ac1942.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push sample_project

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project sample_project --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_s3 --session now

## Local mode

    # Run
    $ td wf run td_s3.dig

# Supplemental

Available parameters for `result_settings` are here.

- bucket: (string, required)
- path: (string, required)
- format: (string(csv|tsv), default csv)
- compression: (string(None|gz), default None)
- header: (boolean, default true)
- delimiter: (string(","|"\t"|"|"), default ",")
- "null": (string("empty"|"\\N"|NULL|null|any characters), default "empty")
- newline: (string(\r\n(CRLF)|\r(CR)|\n(LF)), default \r\n(CRLF))
- quote: (string, optional)
- escape: (string, optional)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-s3#usage)

# Next Step

If you have any questions, please contact support@treasure-data.com.
