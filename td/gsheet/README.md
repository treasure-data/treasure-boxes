# Workflow: td example (Result Output to Google Spreadsheet)

This example workflow exports TD job results into a Google Spreadsheet [Treasure Data's Writing Job Results into Google Spread](https://docs.treasuredata.com/articles/result-into-google-spreadsheet) with [td](http://docs.digdag.io/operators/td.html) operator.

# Prerequisites

Connect Treasure Data user account to your Google Account.
https://docs.treasuredata.com/articles/result-into-google-spreadsheet#authorization


# Running workflow

### Local Testing
    # Set Secrets on your local for testing
    $ td wf secrets --local --set gsheet.password=******
    #Run it locally
    $ td wf run td_gsheet

### Server Testing
    #Push to server
    $ td wf push gsheet
    # Set Secrets
    $ td wf secrets --project gsheet --set gsheet.password=******
    
You can trigger the session manually.

    # Run
    $ td wf start gsheet td_gsheet --session now

# Supplemental

URL format of Result Output to Google Spreadsheet is the following:

- gspreadsheet://user:password@domain.com/sample_spreadsheet/sample_worksheet              # (default: mode=replace)
- gspreadsheet://user:password@domain.com/sample_spreadsheet/sample_worksheet?mode=append  # append


For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-google-spreadsheet)

# Next Step

If you have any questions, please contact support@treasure-data.com.