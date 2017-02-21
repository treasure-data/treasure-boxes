# Workflow: td example (Result Output to s3)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into AWS S3](https://docs.treasuredata.com/articles/result-into-s3) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

You can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_load_example
    
    # Run
    $ td wf start td_load_example daily_load --session now
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
