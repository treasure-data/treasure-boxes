# Workflow: td example (Result Output to Tableau)

This example workflow ingests data using [Tableau Server with Treasure Data](https://docs.treasuredata.com/articles/tableau-server) or [Tableau Online with Treasure Data](https://docs.treasuredata.com/articles/tableau-online) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/36e2c7e98f3b9b800417926c5fb4f6f6.png)

![](https://t.gyazo.com/teams/treasure-data/fcf8d3bf8776ce49486119c70881789a.png)

![](https://t.gyazo.com/teams/treasure-data/1f0d577b1ec1fdf6b25f140edbeaf5b6.png)

The connection name is used in the dig file.

# How to Run

## Server mode

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_tableau

You can trigger the session manually.

    # Run
    $ td wf start td_tableau tableau --session now

## Local mode

    # Run
    $ td wf run tableau.dig

## List of Result Settings
- datasource (required)
- site_id (optional)
- project (optional)

# Next Step

If you have any questions, please contact support@treasuredata.com.
