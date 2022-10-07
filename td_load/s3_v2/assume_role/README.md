# Workflow: td_load Example (Amazon S3 v2)

This sample uses AssumeRole. Details are in the article below:
- [AssumeRole (AWS)](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)

## Note

You have to call the v2 source of Treasure Data console because this feature doesn't allow you to set AssumeRole on yaml file.

The following prearations are required when using AssumeRole.
* Create S3 source on you Treasure Data console with Amazon S3 (v2) connector.
* Set up your IAM role for the auth method.

### How to get Soure ID (Unique ID)

1. In the TD Console, navigate to [Integrations Hub] > [Sources].
2. Select a connector and then select the more menu (...).
3. Select [Copy Unique ID].

See https://docs.treasuredata.com/display/public/PD/Getting+Started+with+Treasure+Workflow for detail.

## How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

# Next Step

If you have any questions, please contact support@treasure-data.com.
