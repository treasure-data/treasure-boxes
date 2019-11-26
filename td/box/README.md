# Workflow: td example (Result Output to Data Tanks)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into BOX](https://support.treasuredata.com/hc/en-us/articles/360010338114-Box-Export) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please confirm `Box` connection is registered in `Integrations Hub -> Authentications` List in Treasure Console.
This example refers to `box_authentications` in Authentications List in Treasure Console

## Local Mode

    # Run on local
    $ td wf run td_box.dig

## Server Mode

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_box

You can trigger the session manually.

    # Run
    $ td wf start td_box --session now

# Supplemental

Available parameters for `result_settings` are here.

- folder_id : (string, required)
- file_ext  : (string, like ".csv")
- file_name : (string)
- mode      : new_file
- formatter :
  - type: (string(csv|tsv), default csv)
  - header_line: (boolean, default true)

# Next Step

If you have any questions, please contact support@treasure-data.com.
