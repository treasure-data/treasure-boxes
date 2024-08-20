# Workflow: Scenario (Generate Impact of Deleting A User Report)

## Scenario

The purpose of this scenario is to generate a report listing the impact on resources owned by a user who will be deleted.

`Deleted Users and the Impact on Existing Resources`:  https://docs.treasuredata.com/articles/#!pd/Deleted-Users-and-the-Impact-on-Existing-Resources

### Limitations
Due to limitations in the API, this report cannot provide resource ownership information for the following resources:
- API keys
- Sources
- Treasure Insights Dashboards

### Prerequisites
This report is dependent on the following monitoring workflows in this scenario:
https://github.com/treasure-data/treasure-boxes/tree/master/scenarios/monitoring
- basic_monitoring
- cdp_monitoring
- insights_monitoring
- workflow_monitoring


### Steps
#### 1. Push the workflow to Treasure Data
```
$ cd impact_of_deleting_user
$ td wf push impact_of_deleting_user
```

#### 2. Configure settings in `common/settings.yaml`
  - `td.database` - the database to write the report to
  - `td.tables.report_table` - the table to write the report to
  - `td.email_to_check` - the user to check for resource ownership and impact upon deletion

### 3. Uncomment data preparation task (if required)
This workflow depends on the monitoring workflows listed in the Prerequisites to download resource data prior to generating the report. If the monitoring workflows have not been run yet, uncomment the `+prepare_data` task to run those workflows now.

#### 4. Register td.apikey as a workflow secret.
```
$ td wf secrets --project impact_of_deleting_user --set td.apikey=<master_api_key>
```

#### 5. Trigger a new session attempt of the workflow
```
$ td wf start impact_of_deleting_user impact_of_deleting_user --session now
```

#### 6. View the report
When the workflow session is completed, the report will be available in the database and table specified in Step 2.