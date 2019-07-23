-- client: molehill/0.0.1
select
  rowid
  , array_concat(
    quantitative_features(
      array("age", "fare")
      , age
      , fare
    ),
    categorical_features(
      array("embarked", "sex", "pclass")
      , embarked
      , sex
      , pclass
    )
  ) as features
  , survived
from
  ${source}
;
