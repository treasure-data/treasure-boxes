# Get RSS feed data and import it to a table 
This workflow gets RSS feed data from web sites you specified and import data to a table. RSS data usually includes contets of web articles. You can utilize those data by tokenize and keyword tagging to users with scores combined with user web activities, for example.

## How to use
### Push workflow and set secret

Download this workflow and push it to your TD environment, then set your td master api key and API server as secret on the project.

```
$ td wf push rss_import
$ td wf secrets --project rss_import --set td.apikey --set td.apiserver
```

|Variable|Description|Example|
|:---|:---|:---|
|`td.apikey`|An API key to be used in the script. Access Type must be `Master Key`.|`1234/abcdefghijklmnopqrstuvwxyz1234567890`|
|`td.apiserver`|TD's API endpoint starting with `https://`. See our [document](https://support.treasuredata.com/hc/en-us/articles/360001474288-Sites-and-Endpoints#Endpoints) for details.|`https://api.treasuredata.com`|

### Set RSS url list
Set rss_url_list you want to get imported in [rss_import.dig](rss_import.dig) file.
Here is example.
```
  rss_url_list: ['https://www.vogue.co.jp/rss/vogue', 'https://feeds.dailyfeed.jp/feed/s/7/887.rss']
```

### Prepare database and table

If you want to change target database and table name, you need to modify following settings in [config/params.yml](config/params.yml) file accordingly.

```
td:
  database: rss_db
  table: rss_tbl
```

### Schedule
You can schedule the workflow with any interval by changing following schedule setting in [rss_import.dig](rss_import.dig) file (set it daily in default).
```
timezone: Asia/Tokyo

schedule:
  daily>: 02:00:00
```

## Output
You can see imported data in rss_db.rss_tbl.
![rss_data](rss_data.png)
