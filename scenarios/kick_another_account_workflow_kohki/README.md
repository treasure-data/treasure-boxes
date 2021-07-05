# Workflow: Run another account's workflow using digdag API

## What is the purpose of this scenario?

Sometimes, you would like to kick workflow which belongs to another Treasure Data account.

You can fulfill such execution using digdag API.
https://docs.digdag.io/api/


## Regarding api_host
"baseurl" in kick_another_account_workflow_kohki.dig is up to your target account's site.
You have to change it if your account's site is located in EU or Tokyo.

Please refer to the doc for more details.
https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints

# How to Run
First, upload the project.

    # Upload
    $ td wf push kick_another_account_workflow_kohki

Second, register target account's api key as a workflow secret.

    # Set secrets
    $ td wf secrets --project kick_another_account_workflow_kohki --set td.another_account_apikey

Now, you can refer to api key as ${secret:td.another_account_apikey}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start kick_another_account_workflow_kohki kick_another_account_workflow_kohki --session now

# Next Step

If you have any questions, please contact [support@treasure-data.com](support@treasure-data.com).
