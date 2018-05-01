## What the workflow did

We prepared three workflows, `predict_logress.dig`, `predict_fm.dig` and `predict_rf.dif`. In order to predict CTRs from a set of features, these workflows employ machine learning algorithm **Logistic Regression**, **Factorization Machines** and **Random Forest**, respectively.

We recommend you to first try `predict_logress.dig` because the number of parameters we need to configure is smaller than `predict_fm.dig`, and exporting Logistic Regression model to external databases such as MySQL is easy for further integration of learnt models and production ad servers.

**Caution:** Currently, Logistic Regression is much more stable and accurate compared to Random Forest in our platform due to an implementation-related issue of underlying OSS library, [Hivemall](https://github.com/apache/incubator-hivemall).

### Data format

Regardless of machine learning algorithm we use, the workflows assume that you already have a table that contains past impressions and users' reactions. For example, our sample table is:

| rowid<br/>`long` | label<br/>`int` | i1<br/>`int` | i2<br/>`int` | ... | c1 (e.g., address) <br/>`string` | c2 (e.g., browser) <br/>`string` | ... |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 0 | 23 | 1 | ... | "Ohio" | "Firefox" | ... |
| 2 | 1 | 18 | 4 | ... | "New York" | "Google Chrome" | ... |
| 3 | 0 | 35 | 44| ... | "California" | "Safari" | ... |
| ... |...|...| ...|...|...|...|...|

In this table, each row represents an impression for an ad, and a column `label` shows user's response to the ad (i.e., clicked or not).

Columns `i1`, `i2`, ... correspond to **integer** (numeric) variables such as age. Meanwhile, columns `c1`, `c2`, ... indicate **categorical** (string) variables like address. All impressions can be represented by a set of the variables (i.e., features) which describes a pair of current user and ad.

Both algorithms take such table as an input and learn "**what kind of features lead clicks**".

### Tasks

`predict_logress.dig` undergoes four steps to build prediction model and evaluate its accuracy:

1. Split all impressions into **80% training** and **20% testing** samples.
	- Both quantitative and categorical features are converted to an array of strings as an input of Logistic Regression.
2. Build a machine learning model using Logistic Regression, and save the model to a new table.
	- In case of Logistic Regression, "model" is weights for features.
3. Predict CTRs for the testing samples in a 0.0-1.0 range.
4. Evaluate the predicted CTRs based on comparisons with correct labels.

The content of `predict_logress.dig` is as follows:

```yml
_export:
  !include : config/params.yml
  td:
    apikey: ${apikey}
    database: ${target}
    engine: hive

# Step 1
+prepare:
  call>: common/prepare_data.dig

+main:
  # Step 2
  +logress_train:
    td>: queries/logress_train.sql
    create_table: logress_model

  # Step 3
  +compute_downsampling_rate:
  td>: queries/downsampling_rate.sql
  engine: presto
  store_last_results: true

  +logress_predict:
    td>: queries/logress_predict.sql
    create_table: prediction

  # Step 4
  +evaluate:
    td>: queries/evaluate.sql
    store_last_results: true

  +show_accuracy:
    echo>: "Logloss (smaller is better): ${td.last_results.logloss}\nArea under the ROC curve (value in [0.7, 0.9] is reasonable): ${td.last_results.auc}"
```

After Step 2, weights for the features are stored in `logress_model`:

| feature | weight |
|:---:|:---:|
| i1      |   0.2616434097290039 |
| i2      |  0.43628165125846863 |
| i3      | 0.001486081164330244 |
| ... | ...|

By using the weights, prediction should be:

| rowid<br/>`long` | predicted_ctr<br/>`double` |
|:---:|:---:|
|80038 |0.487177|
|80043|0.9583734|
|80046 | 0.9104515 |
| ... | ... |


`predict_fm.dig` are actually different from `predict_logress.dig` in terms of algorithm, but basic structure of the workflows is same.

Note that, for efficient computation, features can be passed to hash functions in practice. This strategy is called **feature hashing**. You can learn more about the technique from [HERE](http://hivemall.incubator.apache.org/userguide/ft_engineering/hashing.html), and try it by modifying [preprocess_train.sql](../queries/preprocess_train.sql) and [preprocess_test.sql](../queries/preprocess_test.sql).

### Configurable parameters

You can specify arbitrary source table and target database in `config/general.yml`. In addition, you can configure `pos_oversampling` in the file. This value controls the number of over-sampled positive samples; if you set greater than 1 to the parameter, positive samples will be over-sampled in training step.

```yml
source: criteo_sample.samples # input table
target: criteo_sample # output database

pos_oversampling: 1
```

The following paper describes about the oversampling technique: [Practical Lessons from Predicting Clicks on Ads at Facebook](https://research.fb.com/publications/practical-lessons-from-predicting-clicks-on-ads-at-facebook/)

For `predict_fm.dig`, there are additional parameters we need to set. These are in `config/fm.yml`:

```yml
# Parameters for Factorization Machines:

# (1) Number of latent factors
factors: 8

# (2) Number of iterations
iters: 50

# (3) Regularization parameters:
# In order to achieve better reuslts, it is necessary
# to set these parameters appropriately.
# Too large or small values lead poor accuracy.
lambda_w0: 0.01
lambda_wi: 0.01
lambda_v: 0.01

# (4) Learning rate:
# Too large/small => poor accuracy
eta: 0.01
```

### Evaluating the accuracy of prediction

As a result of our workflows, you will ultimately see an output like:

```
Logloss (smaller is better): 0.4830765741653266
Area under the ROC curve (value in [0.7, 0.9] is reasonable): 0.7316643845183765
```

These values indicates the accuracy of CTR prediction, and smaller `Logloss` or larger `Area under the ROC curve` (AUC) value means that our predictor is better. For testing samples which satisfy `label` is 0 (1), we desire predicted CTR is small (large); the accuracy is computed based on a comparison between the expected and actual result.

It should be noted that exceptionally good AUC value (i.e., more than 0.9) is a bad sign; it indicates the possibility of [data leakage](https://www.kaggle.com/dansbecker/data-leakage), and you should carefully check if your feature representation has no problem.

By default, the accuracy of our workflow examples falls into somewhere around the following values:

|Algorithm<br />`Workflow` | Logloss | AUC |
|:---:|:---:|:---:|
|Logistic Regression<br />`predict_logress.dig`| 0.483 | 0.732 |
|Factorization Machines<br />`predict_fm.dig`| 0.687 | 0.680 |
|RandomForest<br />`predict_rf.dig`| 2.200 | 0.645 |

If you are not satisfied with the accuracy, you can try the same workflow with different parameters by modifying `config/fm.yml`, or different set of variables by changing table schema.

## Data preparation

So far, we used a sample table `criteo_sample.samples` as data source. The impression data is obtained from [Criteo labs](http://labs.criteo.com/2014/02/dataset/).

We prepared a script which enables you to easily get and import the data:

```
$ ./data.sh
```

***Note***: *You first need to agree with their term of use.*