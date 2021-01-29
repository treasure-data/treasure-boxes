# Workflow: td example (Result Output to Data Tanks)

This example workflow exports data to [Data Tanks](https://docs.treasuredata.com/display/public/PD/Data+Tanks+Using+Presto) using [Treasure Data's Writing Job Results into PostgreSQL Table)](https://docs.treasuredata.com/display/public/INT/PostgreSQL+Export+Integration) with [td](https://docs.digdag.io/operators/td.html) operator.

Data Tanks is an add-on feature. Please contact Treasure Data Support if you're interested.

# How to Run

First, please confirm `datatank` connection is registered in Connection List.
This example refers to `datatank` and `datatank_cstore` in Connection List

## Local Mode

    # Run on local
    $ td wf run td_datatank.dig

## Server Mode

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_dataatnk

You can trigger the session manually.

    # Run
    $ td wf start td_postgresql td_postgresql --session now

# Supplemental

Available parameters for `result_settings` are here.

- database: (string, required)
- table: (string, required)
- mode: (string(append|replace|truncate|update), default append)
- unique: (string, available for update mode)
- method: (string(copy|insert), default copy)
- schema: (string, optional)
- fdw: (string(None|cstore), default None)

# Next Step

If you have any questions, please contact support@treasure-data.com.
