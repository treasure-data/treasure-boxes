# Workflow: Scenario (Queries run sequentially)

## Why should you run queries sequentially?
If the scanned table has a lot of records, querying the whole data set consumes a lot of time and resources, which can cause the query to fail due to the resource limitations. If you can divide the query into smaller units, you can reduce the amount of resources it consumes. However, you would need to run the queries at one time in sequence. For such a case, this scenario helps you to run queries one-by-one, in sequence.

## Scenario

The purpose of this scenario is to get monthly ranking of access users per day. Aggregate top 10 users of each day using divided queries. Then to analyze top 10 users of the month using an aggregated table.

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
