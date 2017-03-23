# Workflow: td example (Result Output to Elasticsearch)

This example workflow exports TD job results into Elasticsearch, using [Treasure Data's Writing Job Results into Elasticsearch](https://docs.treasuredata.com/articles/result-into-elasticsearch) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push sample_project

You can trigger the session manually.

    # Run
    $ td wf start sample_project td_elasticsearch --session now
    
# Supplemental

JSON format of Result Output to Elasticsearch is the following.

- {"type":"elasticsearch","nodes":"host1:9300,host2:9300,...","index":"index","index_type":"index_type","mode":"insert"}

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-elasticsearch).

# Next Step

If you have any questions, please contact support@treasure-data.com.
