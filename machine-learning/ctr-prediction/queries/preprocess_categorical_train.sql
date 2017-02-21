select
  rowid,
  feature_hashing(
    array(
      concat("c1#", c1),
      concat("c2#", c2),
      concat("c3#", c3),
      concat("c4#", c4),
      concat("c5#", c5),
      concat("c6#", c6),
      concat("c7#", c7),
      concat("c8#", c8),
      concat("c9#", c9),
      concat("c10#", c10),
      concat("c11#", c11),
      concat("c12#", c12),
      concat("c13#", c13),
      concat("c14#", c14),
      concat("c15#", c15),
      concat("c16#", c16),
      concat("c17#", c17),
      concat("c18#", c18),
      concat("c19#", c19),
      concat("c20#", c20),
      concat("c21#", c21),
      concat("c22#", c22),
      concat("c23#", c23),
      concat("c24#", c24),
      concat("c25#", c25),
      concat("c26#", c26)
    )
  ) as features,
  label
from
  train
;
