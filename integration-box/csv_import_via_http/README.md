# Import CSV formatted File into TreasureData via http directly.
This workflow project including CustomScript (Python) enables you to import csv file provided by http into TreasureData.

# Installation (Setup)
## set parameters in http_csv_download_sample.dig
- url           : set url to get csv file
- database      : set your database name to import into
- table         : set your table name to import into
- column_setting_file: set CSV setting file name.

## Set apikey as secret ()
https://tddocs.atlassian.net/wiki/spaces/PD/pages/223379597/Setting+Workflow+Secrets+from+the+Command+Line

## Edit csv_setting.json
You can change behavior followings.
- replace column name. set from_name and to_name what you want.
- specify ignoring column to import. If you want to ignore, you should change to true from false.

## update workflow project to TreasureData
Submit workflow to TreasureData.
https://tddocs.atlassian.net/wiki/spaces/PD/pages/1083651/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI

## Appendix
You can specify http settings in detail depend on pandas.read_csv function (encoding, compression, and so on).
like `df = pd.read_csv(url, compression = "zip", encoding = "SHIFT_JIS")`.
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
