drop function if exists extract_feature;
drop function if exists extract_value;
drop function if exists sigmoid;

-- temporary use different delimiter
delimiter $$

create function extract_feature(f varchar(255))
  returns int
begin
  declare feature varchar(255);
  if f like '%:%' then
    set feature = substring_index(f, ':', 1);
  else
    set feature = f;
  end if;
  return cast(feature as unsigned);
end $$

create function extract_value(f varchar(255))
  returns double
begin
  declare value double;
  if f like '%:%' then
    set value = cast(substring_index(f, ':', -1) as decimal(10, 6));
  else
    set value = 1.0;
  end if;
  return value;
end $$

create function sigmoid(x double)
  returns double
begin
  return 1.0 / (1.0 + exp(-x));
end $$

-- restore delimiter
delimiter ;
