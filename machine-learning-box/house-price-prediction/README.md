# House pricing Prediction

In this example, we predict house pricing using [Linear Regression predictor](http://hivemall.incubator.apache.org/userguide/regression/general.html).

## Input

In this workflow, we use [Boston house pricing data](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html).

This workflow assume a table as follows:

| crim<br/>`double` | zn<br/>`double` | indus<br/>`double` | chas<br/>`int` | nox<br/>`double` | rm<br/>`double`  | age<br/>`double` | dis<br/>`double`  | rad<br/>`int` | tax<br/>`int` | ptratio<br/>`double` | b<br/>`double` | lstat<br/>`double` | medv<br/>`double` | 
|---------|------|---------|--------|-------|-------|-------|--------|-------|-------|-----------|--------|---------|--------| 
| 0.00632 | 18   | 2.31    | 0      | 0.538 | 6.575 | 65.2  | 4.09   | 1     | 296   | 15.3      | 396.9  | 4.98    | 24     | 
| 0.02731 | 0    | 7.07    | 0      | 0.469 | 6.421 | 78.9  | 4.9671 | 2     | 242   | 17.8      | 396.9  | 9.14    | 21.6   | 
| 0.02729 | 0    | 7.07    | 0      | 0.469 | 7.185 | 61.1  | 4.9671 | 2     | 242   | 17.8      | 392.83 | 4.03    | 34.7   | 
| 0.03237 | 0    | 2.18    | 0      | 0.458 | 6.998 | 45.8  | 6.0622 | 3     | 222   | 18.7      | 394.63 | 2.94    | 33.4   | 
| ... | ...    | ... | ... | ... | ... | ...  | ... | ... | ... | ... | ... | ... | ... | 

`medv`, Median value of owner-occupied homes in $1000's, is the target value for regression. `chas` and `rad` is categorical values, and other features are quantitative.

By default, top 4 correlated columns with `medv` are used. If you want to change explanatory variables, you can modify following file:

- [vectorize_log1p_features.sql](./queries/vectorize_log1p_features.sql)

## Workflow

```sh
$ ./data.sh # prepare sample dataset
$ td wf push regressor # push workflow to TD
$ td wf start regressor regression --session now
```

If you want to run feature selection with py> operator, you can execute as follows:

```sh
$ ./data.sh
$ td wf push regressor
$ td wf secrets --project regressor --set td.apikey --set td.apiserver
# Set secrets from STDIN like: td.apikey=1/xxxxx, td.apiserver=https://api.treasuredata.com
$ td wf start regressor regression-py --session now
```

* [regression.dig](regression.dig) - TD workflow script for regression
* [regression-py.dig](regression-py.dig) - TD workflow script for regression with scikit-learn feature selection
* [search_hyperparams.dig](search_hyperparams.dig) - TD workflow script for searching hyperparameters. You need to run vectorizing before run this workflow.

## Output

This workflow outputs predicted price of houses in `predictions` table as follows:

| rowid<br/>`string` | predicted_price<br/>`double` |
|:---:|:---|
| 1-10 |33.97034232809395|
| 1-121 |30.3377696027913|
| ... |...|

## Conclusion

Treasure Workflow provides an easy way to predict continuous values, like a price or energy consumption, using Linear Regression predictor.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).
