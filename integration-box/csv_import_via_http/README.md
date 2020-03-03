# Import CSV formatted File into TreasureData via http directly.
This workflow project including CustomScript (Python) enables you to import csv file provided by http into TreasureData.

# Installation (Setup)
## set parameters in http_csv_download_sample.dig
- url           : set url to get csv file
- database      : set your database name to import into
- table         : set your table name to import into
- column_setting_file: set CSV setting file name.

## Set apikey as secret ()
https://support.treasuredata.com/hc/en-us/articles/360001266788-Workflows-Secrets-Management

## Edit csv_setting.json
You can change behavior followings.
- replace column name. set from_name and to_name what you want.
- specify ignoring column to import. If you want to ignore, you should change to true from false.

## update workflow project to TreasureData
Submit workflow to TreasureData.  
https://support.treasuredata.com/hc/en-us/articles/360001262207-Treasure-Workflow-Quick-Start-using-TD-Toolbelt-in-a-CLI#Submit%20the%20workflow%20to%20Treasure%20Data

## Appendix
You can specify http settings in detail depend on pandas.read_csv function (encoding, compression, and so on).  
like `df = pd.read_csv(url, compression = "zip", encoding = "SHIFT_JIS")`.  
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
