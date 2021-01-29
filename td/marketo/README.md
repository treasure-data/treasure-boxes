# Workflow: td example (Result Output to Marketo)

This example workflow exports TD job results into Marketo [Treasure Data's Writing Job Results into Marketo](https://docs.treasuredata.com/display/public/INT/Marketo+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

# Prerequisites

The Marketo connection name is required for use in the workflow file.
Create a new Marketo Connection using [Create Connection](https://docs.treasuredata.com/display/public/INT/Marketo+Export+Integration#Create-a-New-Connection) or use your existing connection.


# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_marketo


You can trigger the session manually.

    # Run
    $ td wf start td_marketo td_marketo --session now

## Local mode

    # Run
    $ td wf run td_marketo.dig

# Supplemental

Available parameters for `result_settings` are here.

- headers: description (string, default: null. When empty, the first row will be headers)
- list_id: The ID of the destination list where Leads are added (string, required)
- lookup_field: The optional field that can be used for de-duplication (string, optional, default to email)
- partition_name: The Marketo partition name these new leads belong to (string, optional)
- retry_limit: Retry Limit (integer, optional)
- retry_initial_wait_msec: Retry Initial wait in Milliseconds (integer, optional)
- max_retry_wait_msec: Retry Max wait in milliseconds (integer, optional)
- http_timeout_millis: Max http waiting time in milliseconds (integer, optional)
- upload_chunk_size_in_bytes: Max upload chunk size in bytes (integer, optional)
- batch_max_wait_msec: Batch max wait in milliseconds (integer, optional)

For more details on Result output to Marketo, please see [Treasure Data documentation](https://docs.treasuredata.com/display/public/INT/Marketo+Export+Integration)

# Next Step

If you have any questions, please contact support@treasure-data.com.
