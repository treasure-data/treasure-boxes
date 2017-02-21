Click-Through-Rate Prediction Template
===

Cost Per Acquisition (CPA) is a key metric that matters to marketers. To reduce costs of online advertising, it is needed to improve **Click-Through-Rate (CTR)**.

Our machine learning solution enables you to predict CTR of each ad session by learning a prediction model from past big data, from millions of attributes and billions of training examples.

## Input

For instance, this workflow takes a table of the following form:

| rowid<br/>`long` | label<br/>`int` | i1<br/>`int` | i2<br/>`int` | ... | c1 (e.g., address) <br/>`string` | c2 (e.g., browser) <br/>`string` | ... |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 0 | 23 | 1 | ... | "Ohio" | "Firefox" | ... |
| 2 | 1 | 18 | 4 | ... | "New York" | "Google Chrome" | ... |
| 3 | 0 | 35 | 44| ... | "California" | "Safari" | ... |
| ... |...|...| ...|...|...|...|...|

You can apply this template for arbitrary dataset as long as samples consist of a set of `int` (quantitative) and `string` (categorical) variables.

## Workflow

We prepared a basic workflow for CTR prediction:

```sh
$ ./data.sh # prepare data
$ td wf run predict -p apikey={YOUR_API_KEY}
```

* [predict.dig](predict.dig) - TD workflow script for CTR prediction using [Factorization Machines](https://hivemall.incubator.apache.org/userguide/recommend/movielens_fm.html)
* [config/params.yml](config/params.yml) - defines configurable parameters for the prediction workflow such as `factor` of Factorization Machines.
  
## Output

The output of workflow is a table that contains predicted CTRs for validation samples:

| rowid<br/>`long` | predicted_ctr<br/>`double` |
|:---:|:---:|
|80038 |0.487177|
|80043|0.9583734|
|80046 | 0.9104515 | 
| ... | ... |

## How This Workflow Works

For further reading for algorithm and/or workflow details, please refer [this page](docs/more.md). 

## Conclusion

Treasure Workflow provides an easy way to predict not only CTR but also Conversion Rate (CVR). What you need to prepare is just a training table.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).
