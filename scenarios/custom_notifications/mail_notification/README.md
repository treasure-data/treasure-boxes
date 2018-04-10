# Workflow: Scenario (Custom notification - mail)

## Scenario

The defalt notification is not able to manage addresses by user. So, the purpose of this scenario is to notify via email if workflow fail.

*Steps*
1. Run an incorrect query, then workflow fails.
2. Kick the `_error` task, then mail operator sends notification including error message.
3. Receive notification email.

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.treasuredata.com/articles/workflows)
 - `mail>: operator`: [for_each>: Repeat tasks for values](http://docs.digdag.io/operators/mail.html)
 - `_error: task`: [_error:](http://docs.digdag.io/concepts.html?highlight=_error#dynamic-task-generation-and-check-error-tasks)

# How to use

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push custom_notification

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start custom_notification custom_notification --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
