# Workflow: Scenario (Using Intermediate Table)

## Why should you use Intermediate Table Workflows?
Using an intermediate table is one of the best ways to avoid query performance issues. More than 85% of Presto queries on Treasure Data are recurring queries that process growing data sets at scheduled intervals. You can use incremental queries to generate intermediate tables that speed up the data analysis of continuously growing data. The cumbersome process of processing raw data (e.g. IP address to country) can be done much more efficiently by using intermediate tables where only the ‘new’ data (data that came in since the last query) is processed and appended to the rest of the processed data, rather than processing the entire data every time.  Here are the steps you would take to accomplish this:

1. Create the basis of an intermediate table by processing all the data you have up to a certain point in time
2. Schedule a query that processes new data that came in since the last query and appends to the intermediate table. Example: every day, query the IP address of visitors in the past day to convert them to countries and append the result to the intermediate table.
3. Query the intermediate table for aggregating data
Example: query the intermediate table to create a daily summary of all visitors by country

Steps 2 and 3 can be made into a Treasure Workflow which enables you to define repeatable sets of dependent queries. This way, the incremental data processing and the resulting data export can be organized into a set of scheduled procedure that is less prone to erroneous handling and has reduced end-to-end latency.

You can read additional information:
1. [Efficiently Analyze Infinitely Growing Data with Incremental Queries](https://blog.treasuredata.com/blog/2017/07/25/analyze-infinitely-growing-data-incremental-queries/)
2. [Treasure Workflow Docs](https://blog.treasuredata.com/blog/2017/07/25/analyze-infinitely-growing-data-incremental-queries/)

## Scenario

The purpose of this scenario is to get the number of unique users who accessed the tracked site for the first time.

*Steps*
1. Make an intermediate table from all of the existing data.
2. Run a query against the intermediate table created in the preceeding step.

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.treasuredata.com/articles/workflows)

# How to use

## Initial Load
The initial load file (initial_task.dig) run the first query that creates the intermediate table that subsequent queries will run against.

## Daily Run
The daily run file is scheduled to run every day at 1:00. It performs two tasks. 
	- It updates the intermediate table created by initial_task.dig.
	- Run the query in the analytics.sql file against the intermediate table.

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push intermediate_table

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start bq_to_td main.dig --session now


# Next Step
This is a simple example using only one intermediate table and just one subsequent query. However, you can use workflows and intermediate tables to chain together many sequential queries that normally would be one very large query that consumed a lot of time and resources. Consider workflows and intermediate tables as a possible solution for your large, time and resource consuming jobs. Feel free to contact support for assistance with reviewing any queries to see if workflows can improve performance.  

If you have any questions, please contact to support@treasuredata.com.
