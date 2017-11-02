# Workflow: Scenario (Using Intermediate Table)

Using an intermediate table is one of the best ways to avoid query performance issues.

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
