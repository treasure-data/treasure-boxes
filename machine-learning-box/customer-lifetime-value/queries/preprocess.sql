with cltv as (
  select
    customerid,
    max_by(country, invoicedate) as country,
    sum(unitprice * quantity) as cltv
  from
    ${source}
  group by
    1
),
train_orders as (
  select
    customerid,
    max(invoicedate) as date_last_order,
    min(invoicedate) as date_first_order,
    avg(basket_value) as avg_basket_value,
    avg(basket_size) as avg_basket_size
  from (
    select
      customerid,
      invoiceno,
      invoicedate,
      sum(unitprice * quantity) as basket_value,
      sum(quantity) as basket_size
    from
      ${source}
    where
      quantity > 0
      and invoicedate < '${threshold_date}'
    group by
      1, 2, 3
  ) t1
  group by
    1
),
train_returns as (
  select
    customerid,
    count(distinct invoiceno) as cnt_returns
  from
    ${source}
  where
    quantity < 0
    and invoicedate < '${threshold_date}'
  group by
    1
)
select
  t1.customerid,
  t1.cltv,
  t1.country,
  -- features for training; aggregated in a training period before ${threshold_date}
  date_diff('day', date_parse(t2.date_first_order, '%Y-%m-%d %T'), date_parse(t2.date_last_order, '%Y-%m-%d %T')) as recency,
  t2.avg_basket_value,
  t2.avg_basket_size,
  coalesce(t3.cnt_returns, 0) as cnt_returns,
  if(t3.cnt_returns is null, 0, 1) as has_returned
from
  cltv t1
left join
  train_orders t2
  on t1.customerid = t2.customerid
left join
  train_returns t3
  on t1.customerid = t3.customerid
where
  t1.cltv > 0
