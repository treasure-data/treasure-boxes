# Workflow: td example (Result Output to Redshift)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into AWS Redshift](https://docs.treasuredata.com/articles/result-into-redshift) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/7182257e51f151f315e43e068054284a.png)

![](https://t.gyazo.com/teams/treasure-data/ad057d9e83d9641313a05342b90c0b1c.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push sample_project

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project sample_project --set key=value

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key=value

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_redshift --session now

## Local mode

    # Run
    $ td wf run td_redshift.dig

# Supplemental

Available parameters for `result_settings` are here.

- database: (string, required)
- table: (string, required)
- mode: (string(append|replace|truncate|update), default append)
- unique: (string, available for update mode)
- schema: (string, optional)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-redshift)

# Next Step

If you have any questions, please contact support@treasure-data.com.
