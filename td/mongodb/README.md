# Workflow: td example (Result Output to MongoDB)

This example workflow exports TD job results into MongoDB, using [Treasure Data's Writing Job Results into your Mongodb Collections](https://docs.treasuredata.com/display/public/INT/MongoDB+Collections+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/540af217745127e39c8ef7c46bf172d2.png)

![](https://t.gyazo.com/teams/treasure-data/d0992f457bc80a3bee5121b0f025ad79.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_mongodb

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_mongodb --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_mongodb td_mongodb --session now

## Local mode

    # Run
    $ td wf run td_mongodb.dig

# Supplemental

Available parameters for `result_settings` are here.

- database: (string, required)
- table: (string, required)
- mode: (string(append|replace|truncate|update), default append)
- unique: (string, available for update mode)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/MongoDB+Collections+Export+Integration).

# Next Step

If you have any questions, please contact support@treasure-data.com.
