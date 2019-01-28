1.push workflow to TD 

git clone https://github.com/treasure-data/workflow-examples


2.create a table as data source for test 

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

3.change db & table name in workflow dig file

cd workflow-examples/id_unification
vi id_unification.dig

_export:
  td:
    database: id_unification
    source_tbl: sample_dataset

_export:
  td:
    database: test_id_unification
    source_tbl: source_dataset


4.select sql file to run

      td>: unify_loop.sql
      #td>: unify_loop_heavy.sql

5. push and run workflow id_unification

cd workflow-examples/id_unification
td workflow push id_unification
td wf start id_unification id_unification --session now

6. reasult will be written into new table 
