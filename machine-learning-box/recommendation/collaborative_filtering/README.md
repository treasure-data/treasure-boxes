# Item-based Collaborative Filtering

This document describes how to run [Item-based Collaborative Filtering](http://hivemall.incubator.apache.org/userguide/recommend/item_based_cf.html) by a workflow.

Give a `transaction` table of user-item interactions, the workflow generates tow tables:

- `topk_similar_items`: similar items for each item.
- `topk_recommended_items`: recommndeded items for each user.

## Usage

To push the workflow to TD:

`td wf push collaborative_filtering`

To run the workflow:

`td wf start --session now collaborative_filtering dimsum`

## Input

`Transaction` table representing transaction logs of item purchases for each user (or, user-item interaction such as item page views).

| userid | itemid | tstamp |
|:-:|:-:|:-:|
| 62772 | 1303 | 1111360502 |
| 62772 | 1304 | 1111359404 |
| 62772 | 1321 | 1111358805 |
| 62772 | 1333 | 1111358834 |
| .. | .. | .. |

## Output

`topk_similar_items` for recommending similar items for each item. 


| itemid | similar_items |
|:-:|:-:|
| 1009 |  ["1967","1270","2193","2161","2081"] |
| 1012 |  ["953","1017","2080","1028","1036"] |
| 1023 |  ["1029","2018","3034","2096","1022"] |
| 1034 |    ["1617","2194","1090","1258","2391"] |
| .. | .. |

`topk_recommended_items` for recommending items for each user.

| userid | rec_items |
|:-:|:-:|
| 8  | ["588","3114","1270","593","1197"] |
| 16 | ["2762","2003","2115","1275","1196"] |
| 24 | ["2571","2291","1214","541","1673"] |
| 32 | ["1610","1372","1356","316","1876"] |
| .. | .. |

## Recommendation logic

The recommendation is, in a word, based on similarity of item cooccurence.

More specifically, the recommndation logic first computes approximate cosine similarity in an item-item matrix using [DIMSUM](https://blog.twitter.com/engineering/en_us/a/2014/all-pairs-similarity-via-dimsum.html) algorithm. The elements in the item-item matrix are cooccurence of user purchases/views for each item-item pair.

Then, based on recent user interests (e.g., top-5 recent item purchases or recent item page views) and `topk_similar_items`, recommended items for each user will be computed in `topk_recommended_items`.