# Workflow Scenario (Notify Plural Users with `mail>:` Operator)

## Scenario

The purpose of this scenario is to send notification to plural email addresses. 

*Steps*
1. Create a `.dig` file includes email information.
2. Load the file with `!include` syntax on the main workflow file.
3. Use `mail>:` operator and kick the email.

In this scenario, the following workflow operator is used. Please refer to the documentation for each operator.

 - `email>:` operator
 -- [mail>: Sending email](https://docs.digdag.io/operators/mail.html)
 - `!include` feature
 -- [!include another file](https://docs.digdag.io/workflow_definition.html#include-another-file)

# How to Run for Server/Client Mode

First, please upload the workflow.

    # Upload
    $ td wf push notify_plural_emails

You can trigger the session manually to watch it execute.

    # Run
    $ td wf start notify_plural_emails --session now


# Next Step

If you have any questions, please contact to support@treasuredata.com.
