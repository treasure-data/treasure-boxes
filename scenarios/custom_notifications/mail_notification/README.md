# Workflow: Scenario (Custom notification - mail)

## Scenario

By default the notification on a workflow failure will only go to the owner of the workflow. The purpose of this scenario is to illustrate how to send an email notification to any address when the workflow encounters and error. 

*Steps*
1. Run an incorrect query, then workflow fails.
2. Kick the `_error` task, then mail operator sends notification including error message.
3. Receive notification email.

In this scenario, some workflow operators are used. Please refer to the documentation for each operator.

 - `td>: operator`: [td>: Running Treasure Data Query](https://docs.digdag.io/operators/td.html)
 - `mail>: operator`: [mail>: Sending email](https://docs.digdag.io/operators/mail.html)
 - `_error: task`: [_error:](https://docs.digdag.io/concepts.html?highlight=_error#dynamic-task-generation-and-check-error-tasks)

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
