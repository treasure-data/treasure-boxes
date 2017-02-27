# Workflow: td example (Result Output to Web Server)

This example workflow ingests data using [Treasure Data's Writing Job Results into Web Server)](https://docs.treasuredata.com/articles/result-into-web) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push web_server

Second, please set credential by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project web_server --set web_server.host=hostname
    $ td wf secrets --project web_server --set web_server.port=8080
    $ td wf secrets --project web_server --set web_server.user=username
    $ td wf secrets --project web_server --set web_server.password=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set web_server.host=hostname
    $ td wf secrets --local --set web_server.port=8080
    $ td wf secrets --local --set web_server.user=username
    $ td wf secrets --local --set web_server.password=xyzxyzxyzxyz

Now you can reference these credential by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start web_server web_server --session now
    
# Supplemental

URL format of Result Output to Web Server is the following.

- web://user:pass@domain.com:8080/path1/path2

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-web#for-on-demand-jobs)

# Next Step

If you have any questions, please contact support@treasure-data.com.
