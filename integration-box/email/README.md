# Workflow: mail

This example sends email using [mail operator](http://docs.digdag.io/operators/mail.html).

# How to Run
The mail operator behaves differently in local mode and server mode.
## Local Mode
First, please make your dig file and mail text.

- [send_email.dig](send_email.dig)
- [body.txt](body.txt)

Second, please set the secrets using `td wf secrets` command. The mail operator uses that secrets for sending email. For more details, please see digdag documentation [secrets](http://docs.digdag.io/command_reference.html#secrets) and [mail operator](http://docs.digdag.io/operators/mail.html#secrets).

    # Set Secrets on your local for testing
    $ td wf secrets --local --set mail.host
    $ td wf secrets --local --set mail.port
    $ td wf secrets --local --set mail.username
    $ td wf secrets --local --set mail.password

Now, you can trigger the session manually.

    # Run
    $ td wf run send_email.dig --session now

## Server Mode
In server mode(Treasure Workflow), you don't need to set the secrets because the mail operater uses Treasure Data's mail server. Therefore, you can not specify the "from" email.

Please upload the workflow and trigger the session manually.

    # Upload
    $ td wf push send_email

Now, you can trigger the session manually.

    # Run
    $ td wf start send_email send_email --session now

You can check the workflow status from [Workflow console](https://workflows.treasuredata.com/).

# Next Step

If you have any questions, please contact support@treasure-data.com.
