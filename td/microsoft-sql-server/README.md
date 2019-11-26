# Workflow: td example (Result Output to Microsoft SQL Server)

This example workflow exports TD job results into SQL Server, using [Treasure Data's Writing Job Results into SQL Server tables](https://docs.treasuredata.com/articles/result-into-microsoft-sql-server) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/8a127ce5e761638959c822a69d384f7b.png)

![](https://t.gyazo.com/teams/treasure-data/158223144cabe1bc78ae6a87eccb241f.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_sql_server

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sql_server --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_sql_server td_sql_server --session now

## Local mode

    # Run
    $ td wf run td_sql_server.dig

# Supplemental

Available parameters for `result_settings` are here.

- instance: (string, required**)
- port: (number, required**)
- database: (string, required)
- table: (string, required)
- timezone: (string, default: UTC)
- batch_size: (integer, default: 16777216)
- mode: (string(insert|insert_direct|truncate_insert|replace), default insert)

** Please note the following conditions in regard to the `result_settings`:
- If you are using Azure, omit the instance name and provide the port # only.
- If you are not using Azure and want to use your own instance: please make sure that you can connect to the database using only the instance name, without the port. If the instance name does not work, you have to set the correct port instead of instance.

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-microsoft-sql-server)

# Next Step

If you have any questions, please contact support@treasure-data.com.
