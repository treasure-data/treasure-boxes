select cast(count(rowid) * 0.8 as bigint) as n_train from ${source};
