# Workflow: td example (Result Output to Web Server)

This example workflow ingests data using [Treasure Data's Writing Job Results into Web Server)](https://docs.treasuredata.com/display/public/INT/Web+Server+and+HTTP+PUT+Endpoint+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

In order to register your credential in TreasureData, please create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/cf2af05ee3d8975b41ac4309578ac19d.png)

![](https://t.gyazo.com/teams/treasure-data/15c88d6228088ca2be9a8adbd13f2e40.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push web_server

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](https://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project web_server --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start web_server web_server --session now

## Local mode

    # Run
    $ td wf run web_server.dig

# Supplemental

Available parameters for `result_settings` are here.

- path: (string, required)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/Web+Server+and+HTTP+PUT+Endpoint+Export+Integration#WebServerandHTTPPUTEndpointExportIntegration-ForOn-DemandJobs)

# Next Step

If you have any questions, please contact support@treasure-data.com.
