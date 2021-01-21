# Workflow: td example (Result Output to MySQL)

This example workflow ingests data using [Treasure Data's Writing Job Results into MySQL Table)](https://docs.treasuredata.com/articles/result-into-mysql) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/6c75a02061c43f1e914589b715a9614f.png)

![](https://t.gyazo.com/teams/treasure-data/a35d719f2a781349e5854315a7f6c3e0.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_mysql

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_mysql --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_mysql td_mysql --session now

## Local mode

    # Run
    $ td wf run td_mysql.dig

# Supplemental

Available parameters for `result_settings` are here.

- database: (string, required)
- table: (string, required)
- mode: (string(append|replace|truncate|update), default append)
- replace_with_schema: (boolean, available for replace mode)
- unique: (string, available for update mode)
- use_compression: (boolean, default false)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-mysql#four-modes-to-modify-data-appendreplacetruncateupdate)

# Next Step

If you have any questions, please contact support@treasure-data.com.
