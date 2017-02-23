## What the workflow did

We prepared two workflows, `predict_logress.dig` and `predict_fm.dig`. In order to predict CTRs from a set of features, the former uses a well-known machine learning algorithm called **Logistic Regression**. An algorithm used in the latter workflow, namely **Factorization Machines**, is much more complex.

We recommend you to first try `predict_logress.dig` because the number of parameters we need to configure is smaller than `predict_fm.dig`, and exporting the models to external databases such as MySQL should be easy for further integration of learnt models and production ad servers.

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
  +logress_predict:
    td>: queries/logress_predict.sql
    create_table: prediction

	# Step 4
  +evaluate:
    td>: queries/evaluate.sql
    store_last_results: true

  +show_accuracy:
    echo>: "Logloss (smaller is better): ${td.last_results.logloss}"
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


`predict_fm.dig` is actually different from `predict_logress.dig` in terms of algorithm, but basic structure of the workflows is same.

Note that, for efficient computation, features can be passed to hash functions in practice. This strategy is called **feature hashing**. You can learn more about the technique from [HERE](http://hivemall.incubator.apache.org/userguide/ft_engineering/hashing.html), and try it by modifying [preprocess_train.sql](../queries/preprocess_train.sql) and [preprocess_test.sql](../queries/preprocess_test.sql).

### Configurable parameters

You can specify arbitrary source table and target database in `config/database.yml`:
	
```yml
source: criteo_sample.samples # input table
target: criteo_sample # output database
```

For `predict_fm.dig`, there are additional parameters we need to set. These are in `config/fm.yml`:
	
```yml
# Parameters for Factorization Machines:

# (1) Number of latent factors
factor: 8

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
Logloss (smaller is better): 0.4828375322703703
```

This value indicates the accuracy of CTR prediction, and smaller value means that our predictor is better. 

It should be noted that, for testing samples that `label` is 0, predicted CTR has to be small. On the other hand, if `label` is 1, higher predicted CTR is better.

If you are not satisfied with the accuracy, you can try the same workflow with different parameters by modifying `config/fm.yml`, or different set of variables by changing table schema. 

## Data preparation

So far, we used a sample table `criteo_sample.samples` as data source. The impression data is obtained from [Criteo labs](http://labs.criteo.com/2014/02/dataset/).

We prepared a script which enables you to easily get and import the data:

```
$ ./data.sh
```

***Note***: *You first need to agree with their term of use.*