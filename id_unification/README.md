# What Is It

# How Does IT Work

# How to Use It 

### 1. Push Workflow to TD 

Run the commands below from local PC:

```
git clone https://github.com/treasure-data/workflow-examples
cd workflow-examples/id_unification
td workflow push id_unification
```
Now you uploaded the workflow to TD side and should be able to see it from web console.

### 2. Create a Table as Data Source 

Run the commands below from local PC:

```
td db:create test_id_unification

td query -d test_id_unification -w --type presto "
create table source_dataset 
as select * from (values
('a@domain.com','123','abc'),
('a@domain.com','234','bcd'),
('b@domain.com','234','cde'),
('c@domain1.com','345','def'),
('e@domain1.com','456','def'),
('f@domain1.com','567','efg')
)as a(email,fingerprint_id,td_client_id)
"
```
Now you created table test_id_unification.source_dataset with test data as below:


### 3. Setup Parameters in Workflow Dig File

Modify workflow dig file id_unification.dig on TD side by web-console:

Before:

```
_export:
  td:
    database: xxxx
    source_tbl: xxxx
    loops: xxxx
    id1: xxxx
    id2: xxxx
    id3: xxxx
```
After:

```
_export:
  td:
    database: test_id_unification
    source_tbl: source_dataset
    loops: 10
    id1: email
    id2: fingerprint_id
    id3: td_client_id
```

### 4. Select SQL File to Run

In same dig file, comment unify_loop_heavy.sql and un-comment unify_loop.sql. For most cases, data will be not big since the 3rd time of unification loop, so non-heavy sql statement would work well enough.

```
    +unify_loop:
      engine: hive
      td>: unify_loop.sql
      #td>: unify_loop_heavy.sql
```

### 5. Run Workflow id_unification

```
td wf start id_unification id_unification --session now
```
Alternately, you could do the same on web console.

### 6. Check Result 

Result can be found in a new table "source_dataset_unified". Unified IDs have been assigned to a new column named "td_id".

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/ae9ef1725c495fa737000d08bf4b6cf2.png)](https://treasure-data.gyazo.com/ae9ef1725c495fa737000d08bf4b6cf2)

Then you need to check table "source_dataset_loop_steps". It would be a good result if the last several lines of loops have same rows count, what means the result has 100% accuracy. If not, please consider a greate number setup to parameter "loops". (min.5 ~ max.80)

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/f931cc76c1b7abb9464079befda69975.png)](https://treasure-data.gyazo.com/f931cc76c1b7abb9464079befda69975)




# Q&A

### Q: I have a source table with more than 3 id columns, how to use this workflow ?

You would need to manually add extra columns you want in the following files. The existing columns id1, id2 and id3 would be good examples.

id_unification.dig
extract_distinct_features.sql
enrich_source_data.sql
assign_td_id.sql

### Q: How long will the workflow run ?

It depends on the source data you imported. 


### Q: How big should I configure the parameter "loops" ?

