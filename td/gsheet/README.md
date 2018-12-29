# Workflow: td example (Result Output to Google Spreadsheet)

This example workflow exports TD job results into a Google Spreadsheet [Treasure Data's Writing Job Results into Google Spread](https://support.treasuredata.com/hc/en-us/articles/360009671913-Writing-Job-Results-to-Google-Sheets) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

Create connection setting on [Connector UI](https://console.treasuredata.com/app/connections).

![](https://support.treasuredata.com/hc/article_attachments/360021508813/google_sheet_catalog.png)

![](https://support.treasuredata.com/hc/article_attachments/360013354894/create-connection.png)

You can find more details about creating and mainting your Google sheets connector [here](https://support.treasuredata.com/hc/en-us/articles/360009671913-Writing-Job-Results-to-Google-Sheets)

The connection name is used in the dig file.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_gsheet

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_gsheet --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_gsheet td_gsheet --session now

## Local mode

    # Run
    $ td wf run td_gsheet.dig

# Supplemental

Available parameters for `result_settings` are here.

- spreadsheet_title: (string, destination spreadsheet name, required if spreadsheet_id is not provided)
- spreadsheet_id: (string, destination spreadsheet key, required if spreadsheet_title is not provided)
- sheet_title: (string, title of single sheet to be updated, required)
- mode: (string(replace|append), default replace)

For more details, please see [Treasure Data documentation](https://support.treasuredata.com/hc/en-us/articles/360009671913-Writing-Job-Results-to-Google-Sheets)

# Next Step

If you have any questions, please contact support@treasure-data.com.
