select
  rowid,
  concat_array(
    quantitative_features(
      array(
        "i1", "i2", "i3", "i4", "i5", "i6", "i7",
        "i8", "i9", "i10", "i11", "i12", "i13"
      ),
      rescale(
        if( i1 is null, 0, i1),
        ${td.last_results.train_min1},
        ${td.last_results.train_max1}
      ),
      rescale(
        if( i2 is null, 0, i2),
        ${td.last_results.train_min2},
        ${td.last_results.train_max2}
      ),
      rescale(
        if( i3 is null, 0, i3),
        ${td.last_results.train_min3},
        ${td.last_results.train_max3}
      ),
      rescale(
        if( i4 is null, 0, i4),
        ${td.last_results.train_min4},
        ${td.last_results.train_max4}
      ),
      rescale(
        if( i5 is null, 0, i5),
        ${td.last_results.train_min5},
        ${td.last_results.train_max5}
      ),
      rescale(
        if( i6 is null, 0, i6),
        ${td.last_results.train_min6},
        ${td.last_results.train_max6}
      ),
      rescale(
        if( i7 is null, 0, i7),
        ${td.last_results.train_min7},
        ${td.last_results.train_max7}
      ),
      rescale(
        if( i8 is null, 0, i8),
        ${td.last_results.train_min8},
        ${td.last_results.train_max8}
      ),
      rescale(
        if( i9 is null, 0, i9),
        ${td.last_results.train_min9},
        ${td.last_results.train_max9}
      ),
      rescale(
        if( i10 is null, 0, i10),
        ${td.last_results.train_min10},
        ${td.last_results.train_max10}
      ),
      rescale(
        if( i11 is null, 0, i11),
        ${td.last_results.train_min11},
        ${td.last_results.train_max11}
      ),
      rescale(
        if( i12 is null, 0, i12),
        ${td.last_results.train_min12},
        ${td.last_results.train_max12}
      ),
      rescale(
        if( i13 is null, 0, i13),
        ${td.last_results.train_min13},
        ${td.last_results.train_max13}
      )
    ),
    -- feature_hashing(
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
    -- )
  ) as features,
  label
from
  samples_train
;
