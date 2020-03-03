## Salesforce Lead + Contact Marketing Pipeline Funnel
----
### Overview

This query combines the lead and contact tables from Salesforce while resolving double-counting issues when leads are converted into contacts. The resulting table can be pushed into a BI tool in order to create a marketing funnel to determine an organization's pipeline health.

This table can also be used as the basis for other attribution use-cases where it's necessary to have a full view of all leads and contacts in your system. 

----
###Implementation

Copy the query into your Treasure Data instance and replace fields that contain CHANGE\_ME. Fields without that tag are standard Salesforce names.

----
###Sample Dashboard in Chartio
![Pipeline Trend + Aggregates](https://i.postimg.cc/gJK8HP07/Screen-Shot-2019-08-07-at-12-04-03-PM.png)
![Drilldown by Channel](https://i.postimg.cc/DfP3LpPb/Screen-Shot-2019-08-07-at-12-08-26-PM.png)
