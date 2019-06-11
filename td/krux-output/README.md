# Workflow to Create Daily Batch for Salesforce DMP (Krux) Output

## Use Cases

This workflow is convenient if a Treasure Data customer wants to use Salesforce DMP (Krux) activation from Audience Studio as Segment Activation. See [here for the official documentation](https://treasuredata.zendesk.com/hc/en-us/articles/360020972534).

What this workflow does is that it consolidates the content of all tables in `TD_DB_NAME` whose name starts with `segment`, consolidates them into a single table and outputs it to Salesforce DMP.

It is designed to run once a day since that's how frequently Salesforce DMP processes first party data import.

## Assumptions

- There's a table called `TD_DB_NAME`, which the user can replace the actual name of the table
- Within `TD_DB_NAME`, tables with prefix "segment" have at least two columns: (1) `kuid` which contains Krux ID and (2) `segment_name` which contains the name of Treasure Data segment. These tables typically arise as an activation of a Segment with `segment_name` representing the name of the segment and `kuid` as one of the attributes.
- Salesforce DMP connection has already been configured with name = `KRUX_CONNECTION_NAME_HERE`.

## How to run it

1. Replace all variables in ALL CAPS within `krux-output.dig` with appropriate values.
2. Run `td wf push krux-output`

## How to confirm it's running successfully

Assuming `kuid` field has matching Krux IDs, these IDs should have an additional attribute called `td_segment` within Salesforce DMP UI.