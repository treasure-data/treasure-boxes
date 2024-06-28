# Workflow: Scenario (Import TD object of workflow from REST API)

## Scenario

The purpose of this scenario is to import session/attempt/project/workflow/schedule metadata from REST API.

*Steps*
1. Initial Import session/attempt/project/workflow/schedule metadata from REST API (initial_ingest_session_attempt.dig)
2. Incrementa Import metadata daily (incremental_ingest.dig)

# How to Run for Server Mode

First, please upload the workflow.

## Upload
  $td wf push workflow_monitoring

Second, you register td.apikey as a secret. (Owner of td.apikey must be admin and have all permission for TD functions.)

## Register
  $td wf secrets --project workflow_monitoring --set td.apikey=1234/abcdefg...

## Run
  $td wf start workflow_monitoring initial_ingest_session_attempt --session now

## Caution
You should set lower_limit_session_id option (initial_ingest_session task of initial_ingest_session_attempt workflow) and lower_limit_attempt_id option (initial_ingest_attempt task of initial_ingest_session_attempt workflow) properly. If you set lower ids, initial_ingest_session_attempt workflow may take longer or cause a timeout error.

# Relationships of Table and REST API

| table | REST API|
| ----- | --------|
| attempts  | [/api/attempts](https://docs.digdag.io/api/) |
| projects | [/api/projects](https://docs.digdag.io/api/) |
| schedules | [/api/schedules](https://docs.digdag.io/api/) |
| sessions | [/api/sessions](https://docs.digdag.io/api/) |
| workflows | [/api/workflows](https://docs.digdag.io/api/) |
| revisions | [/api/projects/{id}/revisions](https://docs.digdag.io/api/) |

**projects** , **schedules** , **workflows** and **revisions**table is replaced daily by incremental_ingest.dig.
**attempts** and **sessions** table is imported incrementally.

# Next Step
If you have any questions, please contact to support@treasuredata.com.
