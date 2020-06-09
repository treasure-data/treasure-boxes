select
  customerid,
  array_concat(
    categorical_features(
      array("country", "has_returned"),
      country, has_returned
    ),
    quantitative_features(
      array("recency", "avg_basket_value", "avg_basket_size", "cnt_returns"),
      ln(recency + 1),
      ln(avg_basket_value + 1),
      ln(avg_basket_size + 1),
      ln(cnt_returns + 1)
    )
  ) as features,
  cltv
from
  cltv_${target}
