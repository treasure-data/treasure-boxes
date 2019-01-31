-- add a case statement for each feature to be unified across
insert overwrite table ${td.source_tbl}_unify_loop_0
select 
  distinct features as features
from (
  select 
    array_remove(array(
      case
        when ${id1} is null or ${id1} = '' then null
        else concat('a:', ${id1})
      end,
 
      case
        when ${id2} is null or ${id2} = '' then null
        else concat('b:', ${id2})
      end,
 
      case
        when ${id3} is null or ${id3} = '' then null
        else concat('c:', ${id3})
      end     
    ), null) as features
  from 
    ${td.source_tbl}
) us
where size(features) > 1  -- 1-element row doesn't contribute to unify
;
