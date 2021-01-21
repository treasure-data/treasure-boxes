# Workflow: http for Slack Example

This example workflow notifies calculated data from TreasureData to Slack, using [http](https://docs.digdag.io/operators/http.html) operator.

# Preparation

This example workflow uses [Incoming Webhooks](https://api.slack.com/incoming-webhooks) on Slack.
You can create a webhook url from [here](https://api.slack.com/apps).

Ex. https://hooks.slack.com/services/xxxxx/yyyyy/zzzzzzzzzzzzzz

# How to Run

First, you need to upload the workflow.

    # Upload
    $ td wf push td_slack_example

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_slack_example slack_mention --session now

# Results

This example workflow would send the following message.

![slack](https://i.gyazo.com/d0d87b9b41f45d0b5ed9046c83c54284.png)
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
