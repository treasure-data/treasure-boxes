with cltv as (
  select
    customerid,
    max_by(country, invoicedate) as country,
    sum(unitprice * quantity) as cltv,
    max(invoicedate) as date_last_order,
    min(invoicedate) as date_first_order
  from
    ${source}
  group by
    1
),
orders as (
  select
    customerid,
    avg(basket_value) as avg_basket_value,
    avg(basket_size) as avg_basket_size
  from (
    select
      customerid,
      invoiceno,
      sum(unitprice * quantity) as basket_value,
      sum(quantity) as basket_size
    from
      ${source}
    where
      quantity > 0
    group by
      1, 2
  ) t1
  group by
    1
),
returns as (
  select
    customerid,
    count(distinct invoiceno) as cnt_returns
  from
    ${source}
  where
    quantity < 0
  group by
    1
)
select
  t1.customerid,
  t1.cltv,
  t1.country,
  date_diff('day', date_parse(t1.date_first_order, '%Y-%m-%d %T.%f'), date_parse(t1.date_last_order, '%Y-%m-%d %T.%f')) as recency,
  t2.avg_basket_value,
  t2.avg_basket_size,
  coalesce(t3.cnt_returns, 0) as cnt_returns,
  if(t3.cnt_returns is null, 0, 1) as has_returned
from
  cltv t1
left join
  orders t2
  on t1.customerid = t2.customerid
left join
  returns t3
  on t1.customerid = t3.customerid
where
  t1.cltv > 0
