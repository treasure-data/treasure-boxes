# Workflow: td example (Result Output to Google Sheets)

This example workflow exports TD job results into a Google Sheets with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

You need to create a new Authentication for Google Sheets in advance.
Please refer to the section '2. Account authentication' in the [Treasure Data Documentation](https://support.treasuredata.com/hc/en-us/articles/360009671913-Writing-Job-Results-to-Google-Sheets) in order to find the procedure.

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

- spreadsheet_id: (string, required if `spreadsheet_title` does not exist)
- spreadsheet_title: (string, required if `spreadsheet_id` does not exist)
- spreadsheet_folder: (string, default: null, Either `spreadsheet_id` or `spreadsheet_name` is required.)
- sheet_title: (string, default: null, worksheet name is required)
- mode: (string(append|replace|truncate|update), default: append)
- range: (string, default: A1, ie. top left corner)
**Note:** for `append` mode, it will not take effect since new rows will be appended after last row
- rows_threshold: (integer, default: 50000, maximum: 2000000)
**Note:** Google API has another threshold of 10MB for request payload. Plugin will automatically detect which threshold reaches first.
- value_input_option: (string(RAW|USER_ENTERED), default: RAW)
- set_nil_for_double_nan: (default: true, ie. turn NaN to empty string)

**※You must choose to use either the *****spreadsheet_id***** OR *****spreadsheet_title.***** You cannot use both.**

For more details, please see [Treasure Data documentation](https://support.treasuredata.com/hc/en-us/articles/360009671913-Writing-Job-Results-to-Google-Sheets)

# Next Step

If you have any questions, please contact support@treasure-data.com.
