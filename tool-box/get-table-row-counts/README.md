# Get row count of tables
This workflow gets all row counts of all tables of all databases and store the information into a table on TD. You can have history of row counts of tables to see your data growth trend by scheduling this workflow every day. Also you can use those data to check and detect unexpected data spike.

## How to use
### Push workflow and set secret
Download this workflow and push it to your TD environment, then set your td master api key as secret on the project.
```
$ td wf push get_row_count
$ td wf secrets --project get_row_count --set td.apikey
```

### Prepare database and table
This workflow creates database and table to store the result.

If you want to change name, you need to modify following settings in [get_row_count.dig](get_row_count.dig) file accordingly.
```
  dest_db: td_stats
  dest_table: row_count
```

### Schedule
You can schedule the workflow with any internal by changing following schedule setting in [get_row_count.dig](get_row_count.dig) file (set it daily in default).
```
timezone: Asia/Tokyo

schedule:
  daily>: 02:00:00
```

### TD endpoint
You need to modify td_endpoint setting in [get_row_count.dig](get_row_count.dig) file for your TD region accordingly. See our [document](https://support.treasuredata.com/hc/en-us/articles/360001474288-Sites-and-Endpoints#Endpoints) for details.
```
    td_endpoint: "https://api.treasuredata.com/"
```

## Output
You can see row_count of your tables in td_stats.row_count table.
```
$ td query -Tpresto -dtd_stats 'SELECT * FROM row_count limit 10' -w

+----------------+------------------------+-----------+------------+
| db_name        | table_name             | row_count | time       |
+----------------+------------------------+-----------+------------+
| sample_db      | file_upload_test       | 600       | 1560928571 |
| sample_db      | test_table_rp          | 100000    | 1560928571 |
| sample_db      | www_access             | 5000      | 1560928571 |
| sample_db      | www_access_test        | 5000      | 1560928571 |
| agent_download | deb                    | 341824    | 1560928571 |
| pos            | bumon_mapping          | 28        | 1560928571 |
| pos            | class_mapping          | 126       | 1560928571 |
| pos            | co_occur_ranking_times | 200       | 1560928571 |
| pos            | demo_pos_data          | 278551    | 1560928571 |
| pos            | demo_web_access        | 767484    | 1560928571 |
+----------------+------------------------+-----------+------------+
```
