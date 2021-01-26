# Workflow: Result Output to DoubleClick Bid Manager

This example workflow ingests data using [Writing Job Results into Google DoubleClick Bid Manager on the DoubleClick Data Platform](https://docs.treasuredata.com/display/public/INT/Google+DoubleClick+Bid+Manager+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/aea8b1080bd9dbc8d343d967b0c7d3e5.png)](https://treasure-data.gyazo.com/aea8b1080bd9dbc8d343d967b0c7d3e5)

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/e2479da555ccce101d2941a29ba31449.png)](https://treasure-data.gyazo.com/e2479da555ccce101d2941a29ba31449)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_dbm

You can trigger the session manually.

    # Run
    $ td wf start td_dbm export_dbm --session now

## Local mode

    # Run
    $ td wf run export_dbm.dig

# Supplemental

Available parameters for `result_settings` are here.

- columns: (string, required)
- cookie_column_header: (string, required)
- membership_lifespan: (int, optional)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/Google+DoubleClick+Bid+Manager+Export+Integration)

# Next Step

If you have any questions, please contact support@treasuredata.com.
