with temp1 as (
  select 'max(If(attemptid=''' || attemptid || ''', DATE_DIFF(''second'', DATE_PARSE(startedat, ''%Y-%m-%dT%H:%i:%sZ''), DATE_PARSE(updatedat, ''%Y-%m-%dT%H:%i:%sZ'')), NULL)) as "' || attemptid || '"' as query_fragment from ${td.tables.tasks}
  group by 1
) 
select array_join(array_agg(query_fragment), ',') as query from temp1