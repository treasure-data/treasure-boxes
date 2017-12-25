# Workflow: td_ddl

This example manipulates tables in Treasure Data daily basis.

The workflow uses [td_run](http://docs.digdag.io/operators.html#td-run-treasure-data-saved-queries) operator to execute the saved queries.

# How to Run

Please upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_run_example
    
    # Run
    $ td wf start td_run_example ddl_operations --session now

You can check the workflow status from [Workflow console](https://workflows.treasuredata.com/).

# Next Step

If you have any questions, please contact support@treasure-data.com.
