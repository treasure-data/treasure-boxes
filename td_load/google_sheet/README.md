# Workflow: td_load Example (Google Sheet)

This example workflow ingests data from Google Sheet in daily basis.

The workflow also uses [Secrets](https://docs.treasuredata.com/display/public/PD/Setting+Workflow+Secrets+from+the+Command+Line) feature, so that you don't have to include your datasource credentials to your workflow files.

# How to Run

First, you can upload the workflow.

    # Upload
    $ td wf push td_load_example

# daily_load.dig (without existing authentication)

Second, please set datasource credentials by `td wf secrets` command.
(Alternatively you can use Web console to register secrets)
https://docs.treasuredata.com/display/public/PD/Setting+Workflow+Secrets+from+TD+Console

    # Set Secrets
    $ td wf secrets --project td_load_example --set gsheet.client_id
    $ td wf secrets --project td_load_example --set gsheet.client_secret
    $ td wf secrets --project td_load_example --set gsheet.refresh_token

Now you can reference these credentials by `${secret:}` syntax within yml file for `td_load` operator.

- [config/daily_load.yml](config/daily_load.yml)

Now, you can trigger the session manually.

    # Run
    $ td wf start td_load_example daily_load --session now

## How to Get Google Secrets

When you get your Google secrets to ingest Google sheet data, you have to create credentials and you can acquire them on OAuth playground.

https://developers.google.com/oauthplayground/

# daily_load_with_ existing_authentication.dig (with existing authentication)

Second, please create authentication via TD console. see details -> https://docs.treasuredata.com/display/public/INT/Google+Sheets+Import+Integration#GoogleSheetsImportIntegration-CreateaNewConnection

Then, you can obtain the td authetication id from the access URL, as follows:
![](screenshot1.png)

Finally, you can write td_authentication_id to daily_load_with_existing_authentication.yaml.

- [config/daily_load_with_existing_authentication.yml](config/daily_load_with_existing_authentication.yml)

And you can run the workflow like the following..

    # Run
    $ td wf start td_load_example daily_load_with_existing_authentication --session now

# Next Step

If you have any questions, please contact support@treasure-data.com.
