# Workflow: td_example

This example executes Treasure Data queries in daily basis, against its sample data set `sample_datasets.nasdaq`.

The workflow uses [td](https://docs.digdag.io/operators.html#td-treasure-data-queries) operator.

# How to Run

Please upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_example
    
    # Run
    $ td wf start td_example nasdaq_analysis --session now

You can check the workflow status from [Workflow console](https://workflows.treasuredata.com/).

# Next Step

If you have any questions, please contact support@treasure-data.com.
