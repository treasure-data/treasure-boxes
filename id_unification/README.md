# What Is It

# How Does IT Work

# How to Use It 

## 1. Push Workflow to TD 

Run the commands below from local PC:

```
git clone https://github.com/treasure-data/workflow-examples
cd workflow-examples/id_unification
td workflow push id_unification
```
Now you uploaded the workflow to TD side and should be able to see it from web console.

## 2. Create a Table as Data Source 

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


## 3. Change DB & Table Name in Workflow dig File

Modify workflow dig file id_unification.dig on TD side by web-console:

Before:

```
_export:
  td:
    database: id_unification
    source_tbl: sample_dataset
```
After:

```
_export:
  td:
    database: test_id_unification
    source_tbl: source_dataset
```

## 4. Select SQL File to Run

In same dig file, comment unify_loop_heavy.sql and un-comment unify_loop.sql.
Test data is very small, so we use non-heavy sql statement.

```
td>: unify_loop.sql
#td>: unify_loop_heavy.sql
```

## 5. Run Workflow id_unification

```
td wf start id_unification id_unification --session now
```

## 6. Check Result 

Result can be found in a new table source_dataset_unified.
