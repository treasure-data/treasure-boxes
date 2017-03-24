# Workflow: td example (Result Output to BigQuery)

This example workflow ingests data using [Treasure Data's Writing Job Results into Google BigQuery](https://docs.treasuredata.com/articles/result-into-google-bigquery) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/a44e6519d63b78dbdf7529ad6a5c7f46.png)

![](https://t.gyazo.com/teams/treasure-data/87cf742b9afb364acb5a364a07f91e9c.png)

The connection name is used in the dig file.

# How to Run

## Server mode

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_bigquery

You can trigger the session manually.

    # Run
    $ td wf start td_bigquery export_bigquery --session now

## Local mode

    # Run
    $ td wf run export_bigquery.dig

# TODO

- Write a list of Result Settings

# Next Step

If you have any questions, please contact support@treasuredata.com.
