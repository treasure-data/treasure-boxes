# Workflow: Kill Treasuredata Workflow attempt

### Caution: This example is NOT recommended.

## What is the purpose of this scenario?
To kill the attempt automatically if the attempt violates sla.

# Prerequisity
- python custom scripting is enables in your account

# How to Run
First, upload the project.

    # Upload
    $ td wf push kill_wf_attempt

Second, register the api key as a workflow secret.

    # Set secrets
    $ td wf secrets --project kill_wf_attempt --set td.apikey

Now, you can refer to api key as ${secret:td.apikey}.

Finaly, you can trigger the session manually.

    # Run
    $ td wf start kill_wf_attempt kill_wf_attempt --session now

# Next Step

If you have any questions, please contact [support@treasure-data.com](support@treasure-data.com).
