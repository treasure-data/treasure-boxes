select 
  sessionid,
  id as attemptid, 
  createdat,
  finishedat,
  DATE_DIFF('second', DATE_PARSE(createdat, '%Y-%m-%dT%H:%i:%sZ'), DATE_PARSE(finishedat, '%Y-%m-%dT%H:%i:%sZ')) as duration
from attempts
where TD_INTERVAL(time, '-30d/now')
  and project like '%xxxx%'
  and workflow like '%xxxx%'
  and status = 'success'
order by 1, 2