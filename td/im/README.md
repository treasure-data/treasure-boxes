
# Workflow: td example (Result Output to Intimate Merger)

This example workflow exports TD job results into Intimate Merger with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

You need to create a new Authentication for Intimate Merger in advance.  
Please refer to the section '2. xxxxxxx' in the [Treasure Data Documentation](https://xxxx) in order to find the procedure.

The connection name is used in the dig file.


# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_im

If you want to mask setting, please set it by `td wf secrets` command. For more details, please see [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_im --set key

    # Set Secrets on your local for testing
    $ td wf secrets --local --set key

Now you can use these secrets by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_im td_im --session now

## Local mode

    # Run
    $ td wf run td_im.dig

# Supplemental

Available parameters for `result_settings` are here.

- spreadsheet_id: (string, spreadsheet key is required※)
- spreadsheet_title: (string, spreadsheet name is required※)
- sheet_title: (string, worksheet name is required)
- mode: (string(replace|append), default replace)  

**※You must choose to use either the *****spreadsheet_id***** OR *****spreadsheet_title.***** You cannot use both.**

For more details, please see [Treasure Data documentation](https://support.treasuredata.com/xxxxxx)

# Next Step

If you have any questions, please contact support@treasure-data.com.
