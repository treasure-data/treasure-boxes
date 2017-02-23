# Workflow: td example (Result Output to Another TD Account)

This example workflow ingests data using [Treasure Data's Writing Job Results into TD Table)](https://docs.treasuredata.com/articles/result-into-td) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push another_td_account

Second, please set destination td account's master apikey by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project another_td_account --set another_td_apikey=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set another_td_apikey=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start another_td_account another_td_account --session now
    
# Supplemental

URL format of Result Output to TD is the following.

- td://APIKEY@endpoint/database/table?mode=append

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-td#two-ways-to-modify-data-appendreplace)

# Next Step

If you have any questions, please contact support@treasure-data.com.
