SELECT userid, itemid, rating, rnd
FROM ratings_mf
WHERE rnd > 0.8
;
