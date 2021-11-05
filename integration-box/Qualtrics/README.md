# Qualtrics Integration

[Qualtrics](https://www.qualtrics.com/) is an experience management platform built around survey engine.  While it offers some data management feature built-in, with Treasure Data it will have additional use cases.

1. Import segment data from Treasure Data that was built from data not in Qualtrics (Export from TD workflow)
2. Export survey result data to Treasure Data to analyze and segment users based on data across the business (Import to TD workflow)

## Workflows

### Contact Autoamtion Export workflow (TD to Qualtrics)

[workflows/qualtrics_export](./workflows/qualtrics_export)

#### Prerequisites

- Contact Import Automation is created in Qualtrics.
- A valid Treasure Data master API key is saved as td.apikey in workflow secret.
- A valid Qualtrics API key is saved as qualtrics.apikey in workflow secret.

#### Configuration (qualtrics_auto_export.dig)

|Key|Description|Sample|
|--|--|--|
|td.endpoint|Endpoint for your Treasure Data Account|https://api.treasuredata.com|
|td.database|Database that has source table|qualtrics_segments|
|td.table|The source table (in td.database)|segment_1|
|td.data_timezone|Timezone of timestamps stored in td.table|'JST' (default 'UTC')|
|qualtrics.endpoint|Qualtrics' API endpoint|https://iad1.qualtrics.com/|
|qualtrics.aid|Qualtrics' Contact Automation ID (string starts with 'AU_')|AU_abcdefghijklmno|
|columns|list of list [TD column name, CSV file header name, Qualtrics column TYPE]|(see below)|

Set secrets as below.

|Key|Description|
|--|--|
|td.apikey|TD API key|
|qualtrics.apikey|Qualtrics API key|

Using TD Toolbelt:

```
td workflow secrets --project [WF Project Name] --set td.apikey [TD master API key] --set qualtrics.apikey [Qualtrics API key]
```

#### setting 'columns'

Variable `columns` have list of list that has `[TD column name, CSV file header name, Qualtrics column TYPE]`.  Please see example below.

- TD column name: column name of specified TD table.
- CSV file header name: this is usually same as TD column name if 'example file' used for data mapping is TD table output.
- Qualtrics column TYPE (Optional): Add 'Transaction' as the third element if the data is timestamp and export as 'Transaction Data'

```yaml
  columns: [
    ['contactid', 'contactid',
    ['firstname', 'firstname'],
    ['lastname', 'lastname'],
    ['email', 'email'],
    ['creationdate', 'creationdate', 'Transaction']
  ]
```

### Survey Result Import workflow (Qualtrics to TD)

[workflows/qualtrics_import](./workflows/qualtrics_import)

#### Prerequisites

- Qualtrics project and its result data is available.
- A valid Treasure Data master API key.
- A valid Qualtrics API key.

#### Configuration (qualtrics_auto_export.dig)

|Key|Description|Sample|
|--|--|--|
|td.endpoint|Endpoint for your Treasure Data Account|https://api.treasuredata.com|
|td.database|Database that has source table|qualtrics_results|
|td.table|The source table (in td.database)|survey_data|
|td.convert_to_long|'true' to convert question columns to long format|'true'|
|qualtrics.endpoint|Qualtrics' API endpoint|https://iad1.qualtrics.com/|
|qualtrics.surveyid|Qualtrics' Survey ID (string starts with 'SV_')|SV_abcdefghijklmno|
|qualtrics.columns_to_keep_wide|list of column names to keep as wide format|(see below)|

Set secrets as below.

|Key|Description|
|--|--|
|td.apikey|TD API key|
|qualtrics.apikey|Qualtrics API key|

Using TD Toolbelt:

```
td workflow secrets --project [WF Project Name] --set td.apikey [TD master API key] --set qualtrics.apikey [Qualtrics API key]
```

#### long and wide format

By default, the workflow imports Qualtrics' result data with all answers in one line (wide format) just as exported as CSV from Qualtrics user interface.

```
_recordid,recordeddate,...,Q1D1,Q1D2,...
R_1n7uIsGUlN2R93M,2021-10-21 05:06:20,...,1,2,...
```

However there are cases where question-answer are converted to long format.

```
_recordid,recordeddate,...,question,value
R_1n7uIsGUlN2R93M,2021-10-21 05:06:20,...,Q1D1,1
R_1n7uIsGUlN2R93M,2021-10-21 05:06:20,...,Q1D2,2
```

If `td.convert_to_long` is set to `true`, columns below will be kept wide (appears in every line), while each of other columns are converted to `question` and `value` columns.

- Columns to and include `userlanguage` column
- 'solutionrevision', 'projectcategory', 'projecttype' columns
- Columns listed in `qualtrics.columns_to_keep_wide` (comma-separated string)

