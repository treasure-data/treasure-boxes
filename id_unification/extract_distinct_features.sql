-- add a case statement for each feature to be unified across
insert overwrite table ${td.source_tbl}_unify_loop_0
select distinct features as features
from (
  select array_remove(array(
      case
        when email is null or email = '' then null
        else concat('a:', email)
      end,
 
      case
        when fingerprint_id is null or fingerprint_id = '' then null
        else concat('b:', fingerprint_id)
      end,
 
      case
        when td_client_id is null or td_client_id = '' then null
        else concat('c:', td_client_id)
      end
    ), null) as features
  from ${td.source_tbl}
) us
where size(features) > 1  -- 1-element row doesn't contribute to unify