with u_rnd as (
  select cast(idx as bigint) userid, pu, bu, rand(31) as rnd
  from mf_model m
  where m.idx in (select userid from ratings_mf)
),
i as (
  select cast(idx as bigint) itemid, qi, bi
  from mf_model m
  where m.idx in (select itemid from ratings_mf)
),
t1 as (
  select
    each_top_k(${k}, u.userid, mf_predict(u.pu, i.qi, u.bu, i.bi, ${td.last_results.mu}),
               u.userid, itemid) as (rank, score, userid, itemid)
  from (select userid, pu, bu from u_rnd where rnd < 0.2) u
  left outer join i
  where not exists (
    select userid from training_mf train
    where train.userid = u.userid and train.itemid = i.itemid
  )
),
t2 as (
  select
    each_top_k(${k}, u.userid, mf_predict(u.pu, i.qi, u.bu, i.bi, ${td.last_results.mu}),
               u.userid, itemid) as (rank, score, userid, itemid)
  from (select userid, pu, bu from u_rnd where rnd >= 0.2 and rnd < 0.4) u
  left outer join i
  where not exists (
    select userid from training_mf train
    where train.userid = u.userid and train.itemid = i.itemid
  )
),
t3 as (
  select
    each_top_k(${k}, u.userid, mf_predict(u.pu, i.qi, u.bu, i.bi, ${td.last_results.mu}),
               u.userid, itemid) as (rank, score, userid, itemid)
  from (select userid, pu, bu from u_rnd where rnd >= 0.4 and rnd < 0.6) u
  left outer join i
  where not exists (
    select userid from training_mf train
    where train.userid = u.userid and train.itemid = i.itemid
  )
),
t4 as (
  select
    each_top_k(${k}, u.userid, mf_predict(u.pu, i.qi, u.bu, i.bi, ${td.last_results.mu}),
               u.userid, itemid) as (rank, score, userid, itemid)
  from (select userid, pu, bu from u_rnd where rnd >= 0.6 and rnd < 0.8) u
  left outer join i
  where not exists (
    select userid from training_mf train
    where train.userid = u.userid and train.itemid = i.itemid
  )
),
t5 as (
  select
    each_top_k(${k}, u.userid, mf_predict(u.pu, i.qi, u.bu, i.bi, ${td.last_results.mu}),
               u.userid, itemid) as (rank, score, userid, itemid)
  from (select userid, pu, bu from u_rnd where rnd >= 0.8) u
  left outer join i
  where not exists (
    select userid from training_mf train
    where train.userid = u.userid and train.itemid = i.itemid
  )
)
-- DIGDAG_INSERT_LINE
select * from t1
union all
select * from t2
union all
select * from t3
union all
select * from t4
union all
select * from t5
;
