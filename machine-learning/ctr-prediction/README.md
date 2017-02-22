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

Here, each row represents user's single impression for an ad. Impressions can be written by a set of `int` (quantitative) and `string` (categorical) variables such as users' demographics. A column `label` shows whether a user clicked an ad.

## Workflow

We prepared a basic workflow for CTR prediction:

```sh
$ ./data.sh # prepare data
$ td wf run predict_logress -p apikey={YOUR_API_KEY}
```

* [predict_logress.dig](predict_logress.dig) - TD workflow script for CTR prediction using [Logistic Regression](https://hivemall.incubator.apache.org/userguide/binaryclass/a9a_lr.html)
* [config/params.yml](config/params.yml) - defines configurable parameters for the prediction.
  
## Output

The output of workflow is a table that contains predicted CTRs for possible future impressions:

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
