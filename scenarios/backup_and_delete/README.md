# Workflow: Scenario (Data backup and delete)

## Scenario

The purpose of this scenario is to get backup and delete records for table data optimization.

*Steps*
1. Backup data (INSERT INTO) from active table.
2. Delete data from active table.

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.digdag.io/operators/td.html)

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push backup_and_delete

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start backup_and_delete --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
