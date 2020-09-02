# Workflow/Query samples using Audit log table

Treasure Data provides Audit Log, having all the operations on Treasure Data, such as login, job issues and so on. Because it has so various events and columns, it takes some time and effort to build queries to get information you want.  

This page introduces sample workflow and queries using Audit Log table for possible cases.

### Workflow/Query sample list


|Category|Event|Workflow|Query|Note|
|:----|:----|:----|:----|:----|
|Account Management|Invite new users                              |*|*| |
| |Promoted users to Admin                       |*|*| |
| |Get active users logging in for N days        |*|*| |
| |Get non-active users not logging in for N days|*| |Please use Python version if API version occurs an error. It happens when  a response of API is too large.|
| |Change permission type to FullAccess|*|*| |
| |Attach user to policy|*|*| |
| |Modify policy|*|*| |
|Data Import|Any operation to import data (Except for streaming import)|*|*| |
| |File upload|*|*| |
| |Bulk load with Source|*|*|The case that Source runs triggered by `td_load` is included.|
| |Bulk load with yml file|*|*| |
| |Bulk Import|*|*| |
|Data Export|Result Export Job|*|*| |
| |Result Download on GUI|*|*|Result Download from Job Result and Download History in Activation|
| |Result Download via TD Toolbelt|*|*| |
| |Run Activation|*|*| |
| |Table export|*|*|TD Toolbelt command|
|Create Resources|Authentication|*|*| |
| |Source|*|*| |
| |Database|*|*| |
| |Workflow projects|*|*| |
| |Master Segment|*|*| |
| |Segment|*|*| |
| |Activation|*|*| |
| |Policy|*|*| |
|Others|Jobs with long duration|*|*| |
| |Jobs with query including specific pattern|*|*| |
| |Query issued by pytd|*|*| |

### Documents
- [Premium Audit Log Events](https://tddocs.atlassian.net/wiki/spaces/PD/pages/233734195/Premium+Audit+Log+Events)
- [Premium Audit Log Reference](https://tddocs.atlassian.net/wiki/spaces/PD/pages/208437326/Premium+Audit+Log+Reference)
