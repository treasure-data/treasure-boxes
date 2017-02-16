
Top-k Item Recommendation Template
===

**Top-k recommendation** is an important task to improve customers' engagement in online services. 

This page introduces a workflow template to get top-k item recommendation for each user. You can easily build a recommendation workflow following this guide.

## Input

This workflow takes a table of the following form:

| userid<br/>`long` | itemid<br/>`long` | rating<br/>`float/double` |
|---:|---:|:---:|
|3077|2046|4.0|
|3078|1252|4.0|
|3078|736|1.0|
| ... |...|...|

_**Caution:** `rating` would be the number of clicks/views/conversions/boughts/scores depending on your problem._

The table should be named `input` that includes userid of type `long`, itemid of type `long`, and rating of type `float/double`. 

## Workflow

We prepared a basic workflow for top-k item recommendation.

```sh
$ td wf run recommend.dig -P config/params.yml -p apikey={YOUR_API_KEY} -p database=movielens1m -p table=ratings
```

* [recommend.dig](recommend.dig) - TD workflow script for top-k item recommendation using [Matrix Factorization](https://docs.treasuredata.com/articles/hivemall-movielens20m-mf)
* [config/params.yml](config/params.yml) - defines configurable parameters for the recommendation workflow such as `k` of top-k. By the default, the workflow recommends top-10 items for each user.

[<img src="docs/img/capture.png" alt="capture" max_height=300 />](http://showterm.io/31b8df49efcfbc2bfc5ef#fast)
  
## Output

The output of workflow is a table that contains a list of recommended items for each user as shown below:

| userid<br/>`long` | recommended_items<br/>`array<long>` |
|:---:|:---|
| 10 |[4454,2609,1214,1949,33539,7079,2324,224,3989,26939]|
| 11 |[1035,8580,720,40815,50160,150,3675,31485,8970,7080]|
| 12 |[4886,1721,27611,8636,4226,356,296,2396,2501,6776]|
| ... |...|

## How This Workflow Works

For further reading for algorithm and/or workflow details, please refer [this page](docs/more.md). 

## Conclusion

Treasure Workflow provides an easy way to generate top-k recommendations. What you need to prepare is just a training table.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).
