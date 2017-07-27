# Workflow: td example (Result Output to Google Spreadsheet)

This example workflow exports TD job results into a Google Spreadsheet [Treasure Data's Writing Job Results into Google Spread](https://docs.treasuredata.com/articles/result-into-google-spreadsheet) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

Connect Treasure Data user account to your Google Account.
https://docs.treasuredata.com/articles/result-into-google-spreadsheet#authorization
![](https://t.gyazo.com/teams/treasure-data/0c86ab5766e404f4b4298d3151c5a790.png)

Create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://t.gyazo.com/teams/treasure-data/0570c45ad9128cdea82b8cdbbbf23371.png)

![](https://t.gyazo.com/teams/treasure-data/840088cd65db23178651dcd8d85567c3.png)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_gsheet

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_gsheet --set key=value

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key=value

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_gsheet td_gsheet --session now

## Local mode

    # Run
    $ td wf run td_gsheet.dig

# Supplemental

Available parameters for `result_settings` are here.

- spreadsheet: (string, spreadsheet name or key is required)
- key: (string, spreadsheet key or name is required)
- worksheet: (string, required)
- mode: (string(replace|append), default replace)

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-google-spreadsheet)

# Next Step

If you have any questions, please contact support@treasure-data.com.
