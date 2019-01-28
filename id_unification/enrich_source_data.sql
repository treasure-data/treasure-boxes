insert overwrite table ${td.source_tbl}_enriched
select
  coalesce(
    -- use canonical_id if it is found
    ${td.source_tbl}_unified_id_sets.canonical_id,
    -- otherwise, use the smallest id in the row itself
    data.join_id
  ) as canonical_id,
  data.email,
  data.fingerprint_id,
  data.td_client_id
from (
  select coalesce(
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
        else concat('f:', td_client_id)
      end
    ) as join_id,
    *
  from ${td.source_tbl}
) data
left join ${td.source_tbl}_unified_id_sets on data.join_id = ${td.source_tbl}_unified_id_sets.join_id
