# Workflow: td example (Result Output to Google Spreadsheet)

This example workflow exports TD job results into a Google Spreadsheet with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

You need to create a new Authentication for Google Spread Sheet in advance.  
Please refer to the section '1. Create a Google Sheets export connector in the V3 (current) console' in the [Treasure Data Documentation](https://support.treasuredata.com/hc/en-us/articles/360010360053-Migrating-from-a-Google-Sheets-Legacy-Export-Connector-to-an-OAuth-based-Google-Sheets-Export-Connector).

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

- spreadsheet_id: (string, spreadsheet key is required※)
- spreadsheet_title: (string, spreadsheet name is required※)
- sheet_title: (string, worksheet name is required)
- mode: (string(replace|append), default replace)  

**※You must choose to use either the *****spreadsheet_id***** OR *****spreadsheet_title.***** You cannot use both.**

For more details, please see [Treasure Data documentation](https://support.treasuredata.com/hc/en-us/articles/360010360053-Migrating-from-a-Google-Sheets-Legacy-Export-Connector-to-an-OAuth-based-Google-Sheets-Export-Connector)

# Next Step

If you have any questions, please contact support@treasure-data.com.
