# Customer Profile Enrichment Metrics

----
## Overview

This project provides the workflows necessary to enrich customer profiles with standardized metrics that describe the customer’s behavior. These metrics can then be surfaced within the Treasure Data segment builder to enable marketers to build highly intelligent segments. For an description of each of these metrics, please refer to the Treasure Box overview page for  [Customer Profile Enrichment](https://boxes.treasuredata.com/hc/en-us/articles/360033141254-Customer-Profile-Enrichment)





----
## Implementation
1. Download this folder locally
2. Use [TD Toolbelt](https://support.treasuredata.com/hc/en-us/articles/360001262207-Treasure-Workflow-Quick-Start-using-TD-Toolbelt-in-a-CLI) to upload this folder as a Treasure Workflow project in your Treasure Data account
3. Define the variables listed below to specify what data to process in order to enrich the necessary customer profiles

----
## Reference

In order to run properly, this workflow requires that the user define the following variables:

**user\_master\_table** - the table name of the user master table that contains the customer profiles to be enriched by this workflow

**activity\_table** - the activity table name containing the digital activity of users, such as a pageviews table collected by the Treasure Data JS SDK

**enriched\_user\_master\_table** - the table name given to the enriched user master table created by this workflow

**user\_master\_join\_key** - the column on user\_master\_table that will join to activity\_table\_join\_key

**activity\_table\_join\_key** - the column on activity\_table that will join to user\_master\_join\_key

**td\_intent\_key** - used to calculate td\_intent\_percentile, this column is the timestamp of activity\_table

**utm\_source\_column** - the column on activity\_table that contains a pageview URL with UTM tags. When applying this workflow to a pageview table collected by the Treasure Data JS SDK, this column is 'td\_url'

**nw** - used to calculate td\_avg\_visit\_monthly\_trend, this is the number of weeks over which to calculate the average number of visits. For example, if nw is set as ‘-26w’ it will calculate the avg visits of the page from last 6 months and compare it with current month

**session\_windows\_time** - length of time over which pageviews from the same user should be grouped into a single session

**session\_key** - is the unique user key used to identify a session window (example: td\_client\_id)

**session\_key\_ip** - “td\_ip”, used in conjunction with session\_key to identify a session window


### Note
* This workflow does not alter the original master table. It creates another master table with the enriched customer records

----
## Questions

Please feel free to reach out to support@treasure-data.com with any questions you have about using this code to enrich your customer profiles

