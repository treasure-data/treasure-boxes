# Workflow: Scenario (Ignore failed task)

## What is the purpose of this scenario?
The normal behavior for a workflow is that it should fail if atleast one task in the workflow fails. However there are scenarios where you would want the workflow to skip a failed task and still run to completion. This scenario will allow you to ignore the failed task that caused the error and make the workflow succeed.


## Scenario

The purpose of this scenario is to make the workflow succeed regardless of whether the task fails or not.

*Requirement*
Digdag has 2 types of operators to execute another dig. The `ignore_failure` parameter is supported by `require>` operator only. So you have to use `require>` operator if you want to ignore failure.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.digdag.io/operators/td.html)
 - `require>: [require>: Depends on another workflow](https://docs.digdag.io/operators/require.html)

# How to Run for Server/Client Mode

The [another.dig](another.dig) workflow has made a syntax mistake in SQL to intentionally fail. So, please upload the workflow.

    # Upload
    $ td wf push ignore_failure

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start ignore_failure main --session now

Then, the ignore_failure workflow succeeds even required "failed_task" failed.


# Next Step

If you have any questions, please contact to support@treasuredata.com.
