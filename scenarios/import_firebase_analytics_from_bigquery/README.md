# Workflow: Scenario: Import Firebase analytics from 

## Why should you run queries sequentially?
So far, TreasureData does not have Firebase analytics plugin.
When you want to import Firebase analytics data into TD, you have to import data from BigQuery.
As a Firebase analytics design, Firebase creates a new table everyday, and it makes impossible to import data incrementally.
So, this sample shows how to import Firebase analytics data incrementally.

## Scenario

Import Firebase analytics data from BigQuery to TreasureData.

*Steps*
1. Clear the aggregated table.
2. Run the queries to insert top 10 users per day to aggregated table.
3. Run the query to analyze top 10 users of the month. 

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](http://docs.digdag.io/operators/td.html)
 - `td_ddl: operator`: [td_ddl: Treasure Data operations](http://docs.digdag.io/operators/td_ddl.html)
 - `loop>: operator`: [loop>: Repeat tasks](http://docs.digdag.io/operators/loop.html)

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push sequential_queries

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start bsequential_queries --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
