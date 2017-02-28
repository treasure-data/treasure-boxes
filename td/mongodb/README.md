# Workflow: td example (Result Output to MongoDB)

This example workflow exports TD job results into MongoDB, using [Treasure Data's Writing Job Results into your Mongodb Collections](https://docs.treasuredata.com/articles/result-into-mongodb) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push sample_project

Second, please set credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project sample_project --set mongodb.host=hostname
    $ td wf secrets --project sample_project --set mongodb.port=27017
    $ td wf secrets --project sample_project --set mongodb.user=username
    $ td wf secrets --project sample_project --set mongodb.password=password

    # Set Secrets on your local for testing
    $ td wf secrets --local --set mongodb.host=hostname
    $ td wf secrets --local --set mongodb.port=27017
    $ td wf secrets --local --set mongodb.user=username
    $ td wf secrets --local --set mongodb.password=password

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_mongodb --session now
    
# Supplemental

JSON format of Result Output to MongoDB is the following.

- mongodb://user:password@host:1234/database/collection?mode=append

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-mongodb).

# Next Step

If you have any questions, please contact support@treasure-data.com.
