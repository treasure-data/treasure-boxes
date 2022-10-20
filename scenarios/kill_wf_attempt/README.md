# Workflow: Kill Treasuredata Workflow attempt

### Caution: This example is NOT recommended.

## What is the purpose of this scenario?
To kill the attempt automatically if the attempt violates sla.

## Prerequisity
- python custom scripting is enabled on your account

## Regarding baseurl
"baseurl" in kill_wf_attempt.dig is up to your account's site.
You have to change baseurl if your account's site is EU, Tokyo.

Please refer to the doc for more details.
https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints

# How to Run
First, upload the project.

    # Upload
    $ td wf push kill_wf_attempt

Second, register the api key as a workflow secret.
Pleaes note, you should add `TD1` before your apikey. So, http.authorization should be `TD1 your_api_key`

    # Set secrets
    $ td wf secrets --project kill_wf_attempt --set http.authorization

Now, you can refer to api key as ${secret:td.apikey}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start kill_wf_attempt kill_wf_attempt --session now

# Next Step

If you have any questions, please contact [support@treasure-data.com](support@treasure-data.com).
