# Workflow/Query samples using Audit log table

Treasure Data provides Audit Log, having all the operations on Treasure Data, such as login, job issues and so on. Because it has so various events and columns, it takes some time and effort to build queries to get information you want.  

This page introduces sample workflow and queries using Audit Log table for possible cases.

### Workflow/Query samples


|Category|Event|Workflow|Query|Note|
|:----|:----|:----|:----|:----|
|Account Management|Invite new users                              | [*](/detection_samples.dig#L9) |[*](queries/invite_new_user.sql)| |
| |Promoted users to Admin                       | [*](/detection_samples.dig#L12) |[*](queries/promote_to_admin.sql)| |
| |Get active users logging in for N days        | [*](/detection_samples.dig#L15) |[*](queries/active_users.sql)| |
| |Get non-active users not logging in for N days|[*](/detection_samples.dig#L20)| | |
| |Change permission type to FullAccess| [*](/detection_samples.dig#L48)|[*](queries/promote_to_fullaccess.sql)| |
| |Attach user to policy| [*](/detection_samples.dig#L51)|[*](queries/attach_user_to_policy.sql)| |
| |Modify policy| [*](/detection_samples.dig#L54)|[*](queries/modify_policy.sql)| |
|Data Import|Any operation to import data (Except for streaming import)| [*](/detection_samples.dig#L59)|[*](queries/operation_importing_data.sql)| |
| |File upload|[*](/detection_samples.dig#L62)|[*](queries/file_upload.sql)| |
| |Bulk Import|[*](/detection_samples.dig#L65)|[*](queries/bulk_import.sql)| |
| |Bulk load with Source|[*](/detection_samples.dig#L68)|[*](queries/bulk_load_with_source.sql)|The case that Source runs triggered by `td_load` is included.|
| |Bulk load with yml file| [*](/detection_samples.dig#L71)|[*](queries/bulk_load_with_yml.sql)| |
|Data Export|Result Export Job|[*](/detection_samples.dig#L75)|[*](queries/result_export_job.sql)| |
| |Result Download on GUI|[*](/detection_samples.dig#L78)|[*](queries/result_download.sql)|Result Download from Job Result and Download History in Activation|
| |Result Download via TD Toolbelt|[*](/detection_samples.dig#L81)|[*](queries/result_download_with_toolbelt.sql)| |
| |Run Activation|[*](/detection_samples.dig#L84)|[*](queries/run_activation.sql)| |
| |Table export|[*](/detection_samples.dig#L87)|[*](queries/table_export.sql)|TD Toolbelt's command (`td table:export`)|
|Create Resources|Authentication|[*](/detection_samples.dig#L91)|[*](queries/create_authentication.sql)| |
| |Source|[*](/detection_samples.dig#L94)|[*](queries/create_source.sql)| |
| |Database|[*](/detection_samples.dig#L97)|[*](queries/create_database.sql)| |
| |Workflow projects|[*](/detection_samples.dig#L100)|[*](queries/create_workflow_project.sql)| Cannot distinguish creating and modifying workflows.|
| |Master Segment|[*](/detection_samples.dig#L103)|[*](queries/create_master_segment.sql)| |
| |Segment|[*](/detection_samples.dig#L106)|[*](queries/create_segment.sql)| |
| |Activation|[*](/detection_samples.dig#L109)|[*](queries/create_activation.sql)| |
| |Policy|[*](/detection_samples.dig#L112)|[*](queries/create_policy.sql)| |
|Others|Jobs with long duration|[*](/detection_samples.dig#L116)|[*](queries/get_long_duration_job.sql)| |
| |Jobs with query including specific pattern|[*](/detection_samples.dig#L121)|[*](queries/get_job_with_query_matching_pattern.sql)| |
| |Query issued by pytd|[*](/detection_samples.dig#L126)|[*](queries/get_job_issued_by_pytd.sql)| | |

#### `audiglog_example.dig`
This file is a workflow to run all the task above. When trying it, please set following parameters.

| Paramater | Value |
| ---- | ---- |
| td.endpoint | - api.treasudata.com <br> - api.treasuredata.co.jp <br> -  api.eu01.treasuredata.com <br> -  api.ap02.treasuredata.com  |
|secret:td.apikey | 1/xxxx |

### Documents
- [Premium Audit Log Events](https://tddocs.atlassian.net/wiki/spaces/PD/pages/233734195/Premium+Audit+Log+Events)
- [Premium Audit Log Reference](https://tddocs.atlassian.net/wiki/spaces/PD/pages/208437326/Premium+Audit+Log+Reference)
