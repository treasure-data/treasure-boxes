select *
from ${source}
where rowid > ${td.last_results.n_train} and label = 1
order by rowid asc
;
