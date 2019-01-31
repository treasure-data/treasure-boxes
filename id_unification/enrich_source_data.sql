insert overwrite table ${td.source_tbl}_enriched
select
  coalesce(
    -- use canonical_id if it is found
    ${td.source_tbl}_unified_id_sets.canonical_id,
    -- otherwise, use the smallest id in the row itself
    data.join_id
  ) as canonical_id,
  data.${id1},
  data.${id2},
  data.${id3}
from (
  select coalesce(
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
    ) as join_id,
    *
  from ${td.source_tbl}
) data
left join ${td.source_tbl}_unified_id_sets on data.join_id = ${td.source_tbl}_unified_id_sets.join_id
