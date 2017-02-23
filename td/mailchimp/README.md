# Workflow: td Example (Result Output to Mailchimp)

[Our blog post](https://blog.treasuredata.com/blog/2016/08/31/increase-customer-engagement-with-mailchimp/) describes an importance of customer engagement with Mailchimp and Treasure Data

This example workflow gives you an overview and directions on how to build personalized email lists on Mailchimp using [Treasure Data's Result Output to Mailchimp](https://docs.treasuredata.com/articles/result-into-mailchimp) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

The workflow also uses [Secrets](https://docs.treasuredata.com/articles/workflows-secrets) feature, so that you don't have to include your database credentials to your workflow files.

First, please set Mailchimp apikey by `td wf secrets` command.

    # Set Secret for server mode
    $ td wf secrets --project td_mailchimp_example --set mailchimp.apikey=xxxxxx
    # Set Secret for local mode
    $ td wf secrets --local --set mailchimp.apikey=xxxxxx

Now you can reference these credentials by `${secret:mailchimp.apikey}` syntax within yml file for `td` operator.

Then, you need to upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_mailchimp_example
    
    # Run on Server
    $ td wf start td_mailchimp_example mailchimp_export --session now
    # Run on Local
    $ td wf run mailchimp_export

# Next Step

If you have any questions, please contact support@treasuredata.com.
