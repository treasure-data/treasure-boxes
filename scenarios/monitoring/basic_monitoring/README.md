# Workflow: Scenario (Import Job/Schedule/Connection from REST API)

## Scenario

The purpose of this scenario is to import Job/Schedule/Connection metadata from REST API.

*Steps*
1. Initial Import Job/Schedule/Connection metadata from REST API (initial_ingest.dig)
2. Incrementa Import metadata daily (incremental_ingest.dig)

# How to Run for Server Mode

First, please upload the workflow.

## Upload
  $td wf push basic_monitoring

Second, you register td.apikey as a secret.

## Register
  $td wf secrets --project basic_monitoring --set td.apikey=1234/abcdefg...

## Run
  $td wf start basic_monitoring initial_ingest --session now

## Caution
  You should set lower_job_id option (initial_ingest_jobs task of initial_ingest workflow) properly.
  If you set lower id, initial_ingest workflow may take longer or cause a timeout error.

# Relationships of Table and REST API

| table | REST API|
| ----- | --------|
| jobs  | [Get Jobs](https://api-docs.treasuredata.com/pages/td-api/tag/Jobs/#tag/Jobs/operation/getJobs) |
| connections | [Get connections](https://api-docs.treasuredata.com/pages/td-api/tag/Connections/#tag/Connections/operation/getConnections) |
| schedules | [Get schedules](https://api-docs.treasuredata.com/pages/td-api/tag/Schedules/#tag/Schedules/operation/getSchedules) |

**connections** and **schedules** table is replaced daily by incremental_ingest.dig.
**jobs** table is imported incrementally.

# Next Step
If you have any questions, please contact to support@treasuredata.com.
