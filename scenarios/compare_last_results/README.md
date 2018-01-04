# Workflow: Scenario (Compare the results of td jobs)

## Scenario

The purpose of this scenario is to compare the results of different td queries.
The `store_last_results` can store the first 1 row of the query results to ${td.last_results} variable. However it will be unavailable if following `td>` operator uses `store_last_results`. If you want to compare the last results between different jobs, you need to split the tasks.

*Steps*
1. Run a query with `store_last_results` parameter.
2. Keep a stored last result to variable using `for_each>` operator.
3. Run an another query with `store_last_results` parameter as subtask in `for_each>`.
4. Compare the results using `if>` operator.

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.treasuredata.com/articles/workflows)
 - `for_each>: operator`: [for_each>: Repeat tasks for values](http://docs.digdag.io/operators/for_each.html)
 - `if>: operator`: [if>: Conditional execution](http://docs.digdag.io/operators/if.html)

# How to use

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push compare_last_results

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start compare_last_results step1 --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
