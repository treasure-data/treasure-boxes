# Workflow: Scenario (Import TD Insights object from REST API)

## Scenario

The purpose of this scenario is to import /reporting/datamodels metadata from REST API.

*Steps*
1. Import /reporting/datamodels metadata from REST API (ingest.dig)

# How to Run for Server Mode

First, please upload the workflow.

## Upload
  $td wf push insights_monitoring

Second, you register td.apikey as a secret. (Owner of td.apikey must be admin and have all permission for TD functions.)

## Register
  $td wf secrets --project insights_monitoring --set td.apikey=1234/abcdefg...

## Run
  $td wf start insights_monitoring ingest --session now

# Relationships of Table and REST API

| table | REST API|
| ----- | --------|
| datamodels  | [/api/reporting/datamodels] (https://docs.treasuredata.com/articles/#!pd/reference-insights-model-endpoints/a/h1_125997694) |

# Next Step
If you have any questions, please contact to support@treasuredata.com.
