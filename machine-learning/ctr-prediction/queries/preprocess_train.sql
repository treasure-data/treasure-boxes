select
  rowid,
  concat_array(
    quantitative_features(
      array(
        "i1", "i2", "i3", "i4", "i5", "i6", "i7",
        "i8", "i9", "i10", "i11", "i12", "i13"
      ),
      rescale(
        coalesce(i1, 0.0),
        ${td.last_results.train_min1},
        ${td.last_results.train_max1}
      ),
      rescale(
        coalesce(i2, 0.0),
        ${td.last_results.train_min2},
        ${td.last_results.train_max2}
      ),
      rescale(
        coalesce(i3, 0.0),
        ${td.last_results.train_min3},
        ${td.last_results.train_max3}
      ),
      rescale(
        coalesce(i4, 0.0),
        ${td.last_results.train_min4},
        ${td.last_results.train_max4}
      ),
      rescale(
        coalesce(i5, 0.0),
        ${td.last_results.train_min5},
        ${td.last_results.train_max5}
      ),
      rescale(
        coalesce(i6, 0.0),
        ${td.last_results.train_min6},
        ${td.last_results.train_max6}
      ),
      rescale(
        coalesce(i7, 0.0),
        ${td.last_results.train_min7},
        ${td.last_results.train_max7}
      ),
      rescale(
        coalesce(i8, 0.0),
        ${td.last_results.train_min8},
        ${td.last_results.train_max8}
      ),
      rescale(
        coalesce(i9, 0.0),
        ${td.last_results.train_min9},
        ${td.last_results.train_max9}
      ),
      rescale(
        coalesce(i10, 0.0),
        ${td.last_results.train_min10},
        ${td.last_results.train_max10}
      ),
      rescale(
        coalesce(i11, 0.0),
        ${td.last_results.train_min11},
        ${td.last_results.train_max11}
      ),
      rescale(
        coalesce(i12, 0.0),
        ${td.last_results.train_min12},
        ${td.last_results.train_max12}
      ),
      rescale(
        coalesce(i13, 0.0),
        ${td.last_results.train_min13},
        ${td.last_results.train_max13}
      )
    ),
    categorical_features(
      array(
        "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10",
        "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20",
        "c21", "c22", "c23", "c24", "c25", "c26"
      ),
      coalesce(c1, '-'),
      coalesce(c2, '-'),
      coalesce(c3, '-'),
      coalesce(c4, '-'),
      coalesce(c5, '-'),
      coalesce(c6, '-'),
      coalesce(c7, '-'),
      coalesce(c8, '-'),
      coalesce(c9, '-'),
      coalesce(c10, '-'),
      coalesce(c11, '-'),
      coalesce(c12, '-'),
      coalesce(c13, '-'),
      coalesce(c14, '-'),
      coalesce(c15, '-'),
      coalesce(c16, '-'),
      coalesce(c17, '-'),
      coalesce(c18, '-'),
      coalesce(c19, '-'),
      coalesce(c20, '-'),
      coalesce(c21, '-'),
      coalesce(c22, '-'),
      coalesce(c23, '-'),
      coalesce(c24, '-'),
      coalesce(c25, '-'),
      coalesce(c26, '-')
    )
  ) as features,
  label
from
  samples_train
;
