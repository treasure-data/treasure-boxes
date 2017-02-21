select
  rowid,
  array_remove(array(
    if(c1 is null, null, cast( mhash(concat("c1:", c1)) as string) ),
    if(c2 is null, null, cast( mhash(concat("c2:", c2)) as string) ),
    if(c3 is null, null, cast( mhash(concat("c3:", c3)) as string) ),
    if(c4 is null, null, cast( mhash(concat("c4:", c4)) as string) ),
    if(c5 is null, null, cast( mhash(concat("c5:", c5)) as string) ),
    if(c6 is null, null, cast( mhash(concat("c6:", c6)) as string) ),
    if(c7 is null, null, cast( mhash(concat("c7:", c7)) as string) ),
    if(c8 is null, null, cast( mhash(concat("c8:", c8)) as string) ),
    if(c9 is null, null, cast( mhash(concat("c9:", c9)) as string) ),
    if(c10 is null, null, cast( mhash(concat("c10:", c10)) as string) ),
    if(c11 is null, null, cast( mhash(concat("c11:", c11)) as string) ),
    if(c12 is null, null, cast( mhash(concat("c12:", c12)) as string) ),
    if(c13 is null, null, cast( mhash(concat("c13:", c13)) as string) ),
    if(c14 is null, null, cast( mhash(concat("c14:", c14)) as string) ),
    if(c15 is null, null, cast( mhash(concat("c15:", c15)) as string) ),
    if(c16 is null, null, cast( mhash(concat("c16:", c16)) as string) ),
    if(c17 is null, null, cast( mhash(concat("c17:", c17)) as string) ),
    if(c18 is null, null, cast( mhash(concat("c18:", c18)) as string) ),
    if(c19 is null, null, cast( mhash(concat("c19:", c19)) as string) ),
    if(c20 is null, null, cast( mhash(concat("c20:", c20)) as string) ),
    if(c21 is null, null, cast( mhash(concat("c21:", c21)) as string) ),
    if(c22 is null, null, cast( mhash(concat("c22:", c22)) as string) ),
    if(c23 is null, null, cast( mhash(concat("c23:", c23)) as string) ),
    if(c24 is null, null, cast( mhash(concat("c24:", c24)) as string) ),
    if(c25 is null, null, cast( mhash(concat("c25:", c25)) as string) ),
    if(c26 is null, null, cast( mhash(concat("c26:", c26)) as string) )
  ), null) as features,
  label
from
  train
;
