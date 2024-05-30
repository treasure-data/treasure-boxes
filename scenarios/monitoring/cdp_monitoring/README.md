# Workflow: Scenario (import TD objects of CDP from REST API.)

## Scenario

The purpose of this scenario is to import parent segment/entities/journey_statistics metadata from REST API.

*Steps*
1. Initial import parent segment/entities/journey_statistics metadata from REST API (initial_ingest.dig)
2. Incrementa import metadata daily (incremental_ingest.dig)

# How to Run for Server Mode

First, please upload the workflow.

## Upload
  $td wf push cdp_monitoring

Second, you register td.apikey as a secret. (Owner of td.apikey must be admin and have all permission for TD functions.)

## Register
  $td wf secrets --project cdp_monitoring --set td.apikey=1234/abcdefg...

## Run
  $td wf start cdp_monitoring initial_ingest --session now

# Relationships of Table and REST API

| table | REST API|
| ----- | --------|
| entities  | [Retrieve list of objects under specified folder](https://api-docs.treasuredata.com/pages/audience_api_v1/tag/Folders/paths/~1entities~1by-folder~1%7BfolderId%7D/get/) |
| journey_statistics | [Retrieve journey statistics](https://api-docs.treasuredata.com/pages/audience_api_v1/tag/Journeys/paths/~1entities~1journeys~1%7BjourneyId%7D~1statistics/get/) |
| parent_segments | [Retrieve list of parent segments](https://api-docs.treasuredata.com/pages/audience_api_v1/tag/Parent-Segments/paths/~1entities~1parent_segments/get/) |

**entities** , **journey_statistics** and **parent_segments** table is imported incrementally.

# Next Step
If you have any questions, please contact to support@treasuredata.com.