# Workflow: td example (Result Output to Google Cloud Storage)

This example workflow ingests data using [Treasure Data's Writing Job Results into Google Cloud Storage](https://docs.treasuredata.com/articles/result-into-google-cloud-storage) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

The connection name is used in the dig file.

# How to Run

## Server mode

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_gcs

You can trigger the session manually.

    # Run
    $ td wf start td_bigquery export_gcs --session now

## Local mode

    # Run
    $ td wf run export_gcs.dig

# TODO

- Write a list of Result Settings

# Next Step

If you have any questions, please contact support@treasuredata.com.
