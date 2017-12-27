# Workflow: Scenario (Queries run sequentially)

## Why should you run queries sequentially?
If the scanned table has a lot of records, querying to whole data takes a lot of time and resources. And it has possibilities to fail due to the resource shortage. If you can divide the query to small unit, the consumed resource can be decreased. However, you have to run divided queries one-by-one. For such a case, this scenario helps you to run queries one-by-one based on the units.

## Scenario

The purpose of this scenario is to get monthly ranking of access users per day. Aggregate top 10 users of each day using divided queries. Then to analyze top 10 users of the monthi using aggregated table.

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
