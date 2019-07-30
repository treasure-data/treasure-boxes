# Tips for ML workflows

In this document, you will learn common practices for machine learning using Hivemall and Treasure Workflow.

- [Train test split](#train-test-split)
  * [Random sampling](#random-sampling)
  * [Stratified sampling](#stratified-sampling)
- [Feature engineering for continuous values](#feature-engineering-for-continuous-values)
  * [Normalization](#normalization)
    + [Log-transformation (log1p)](#log-transformation-log1p)
    + [Min-max scaling](#min-max-scaling)
    + [Standardization](#standardization)
- [Feature hashing and Feature Quantification](#feature-hashing-and-feature-quantification)
  * [Label encoding for categorical variables](#label-encoding-for-categorical-variables)
- [Missing value imputation: How to handle missing data](#missing-value-imputation-how-to-handle-missing-data)
  * [Categorical data](#categorical-data)
  * [Continuous data](#continuous-data)
- [Other features](#other-features)
- [Parameter tuning](#parameter-tuning)
  * [Grid search](#grid-search)
  * [Random search](#random-search)


## Train test split

Train test split is a common operation for evaluating prediction models. In this section, you learn how to split a dataset into a training set and test set using random sampling or stratified sampling.

### Random sampling

Random sampling is a simple way to split data.

    # prepare.dig
    _export:
      train_sample_rate: 0.8
    
    +shuffle:
      td>: queries/shuffle.sql
      engine: presto
      create_table: samples_shuffled
    
    +split:
      _parallel: true
    
      +train:
        td>: queries/split_train.sql
        engine: presto
        create_table: samples_train
    
      +test:
        td>: queries/split_test.sql
        engine: presto
        create_table: samples_test

In shuffle.sql, we add a random float number distributed uniformly from 0.0 to 1.0 for each row.

    -- Presto: queries/shuffle.sql
    select
      *,
      rand() as rand
    from
      source_table
    ;

Presto doesn't have a way to use a random seed. If you want to split a reproducible way, use Hive instead.

`rowid()` function assigns a unique id for each row. Although `select *` could include [v columns](https://support.treasuredata.com/hc/en-us/articles/360001266468-Schema-Management#Understanding%20the%20TD%20Default%20Schema%C2%A0), it's better to specify target columns, respectively.

    -- Hive: queries/shuffle.sql
    select
      rowid() as rowid
      , column_1
      , column_2
      , column_3
      rand(42) as rand -- 42 is random seed
    from
      source_table
    ;

In `prepare.dig`, `${train_sample_rate}` is set to 0.8. Then, the following query splits 80% of data for the training set and 20% for the test set.

    -- Presto: queries/split_train.sql
    select *
    from samples_shuffled
    where rnd <= ${train_sample_rate}
    ;

    -- Presto: queries/split_test.sql
    select *
    from samples_shuffled
    where rnd > ${train_sample_rate}
    ;

### Stratified sampling

Stratified (random) sampling is another method of sampling that divides a population into smaller subgroups. The original characteristics of distribution are preserved in the subgroups.

The steps to apply stratified sampling is similar to random sampling. Here is an example workflow.

    # prepare.dig
    _export:
      train_sample_rate: 0.8
    
    +shuffle:
      td>: queries/shuffle.sql
      engine: presto
      create_table: samples_shuffled
    
    +split:
      _parallel: true
    
      +train:
        td>: queries/split_train.sql
        engine: presto
        create_table: samples_train
    
      +test:
        td>: queries/split_test.sql
        engine: presto
        create_table: samples_test

Here is a preprocessing step to apply stratified sampling.

    -- Presto: queries/shuffle_stratified.sql
    select
      *,
      -- for stratified sampling
      count(1) over (partition by label) as per_label_count,
      rank() over (partition by label order by rand()) as rank_in_label
    from
      source_table
    ;

Then, the following queries apply stratified sampling to split data into training sets and test sets.

    -- Presto: queries/split_train_stratified.sql
    select *
    from samples_shuffled
    where rank_in_label <= (per_label_count * ${train_sample_rate})
    ;

    -- Presto: queries/split_test_stratified.sql
    select *
    from samples_shuffled
    where rank_in_label > (per_label_count * ${train_sample_rate})
    ;

## Feature engineering for continuous values

### Normalization

When applying linear predictors (link), quantitative variables (e.g., height:172) should be normalized to get better prediction results. Without normalization, the optimization process of supervised learning might not converge, resulting in poor prediction accuracy.

#### Log-transformation (log1p)

Log-transformation is the most simple approach for normalization to avoid unintentional large and/or small numbers that are hard to use in optimization processes.

Using `ln(1+x)` (a.k.a. [log1p](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log1p)) is a popular way to avoid `ln(0)` for both explanatory variables and target variables. Note that `exp(ln(1+x))-1` equals to `x`.

`x` is assumed to be greater than -1.

Here is an example query applying log-transformation.

    -- Hive
    select
      rowid
      , quantitative_features(
        array("indus","rm","ptratio","lstat")
        -- log1p normalization for numerical values
        ,ln(indus + 1) as indus_log1p
        ,ln(rm + 1) as rm_log1p
        ,ln(ptratio + 1) as ptratio_log1p
        ,ln(lstat + 1) as lstat_log1p
      ) as features
      ,price
    from
      raw_table
    ;

In regression problems, target variable `y` can be converted into `ln(1+y)` in training, and predicted value `y^` is converted to `exp(y^)-1` in prediction. If you converted target values in training, you need to apply `exp(y^)-1`, so called [exp1m](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/expm1), for predicted values.

    -- Presto: normalization with log1p
    select
      rowid
      , features
      , ln(price + 1) as price_log1p -- target value
    from
      raw_table
    ;

    -- Presto: Inverse transformation with expm1
    select
      rowid
      ,exp(price_log1p) - 1 as price
    from
      normalized_table
    ;

#### Min-max scaling

Min-max scaling is used for normalization. The following workflow applies min-max scaling. We assume there are two numerical columns: i1 and i2.

    +minmax:
      +train:
        td>: queries/minmax_train.sql
        engine: presto
        store_last_results: true
    
      +test:
        td>: queries/minmax_test.sql
        engine: presto
        store_last_results: true

For training data, you can use the following query.

    -- Presto: queries/minmax_train.sql
    select
      min(i1) as train_min1, max(i1) as train_max1,
      min(i2) as train_min2, max(i2) as train_max2
    from
      samples_train
    ;

For test data, there are several approaches to normalize the data. One is using the same scaling for training data. This approach assumes both training data and test data have the same distribution; otherwise, test data can be out of the range between 0 and 1.

Another approach is to normalize test data considering test data's minimum and maximum. This way can normalize test data between 0 to 1 strictly. To do this, execute the following query.

    -- Presto: queries/minmax_test.sql
    select
      -- carrying over the previous "last_results" (= min-max for training)
      ${td.last_results.train_min1} as train_min1,
      ${td.last_results.train_max1} as train_max1,
      ${td.last_results.train_min2} as train_min2,
      ${td.last_results.train_max2} as train_max2,
      -- min-max for testing should be computed on all of observed samples (i.e., train + test samples)
      least(min(i1), ${td.last_results.train_min1}) as test_min1,
      greatest(max(i1), ${td.last_results.train_max1}) as test_max1,
      least(min(i2), ${td.last_results.train_min2}) as test_min2,
      greatest(max(i2), ${td.last_results.train_max2}) as test_max2
    from
      samples_test
    ;

You can create a train/test table as follows:

    +preprocess:
      _parallel: true
    
      +train:
        td>: queries/preprocess_train.sql
        create_table: train
    
      +test:
        td>: queries/preprocess_test.sql
        create_table: test

Here is an example SQL.

    -- Hive: queries/preprocess_train.sql
    select
      rowid,
      quantitative_features(
        array("i1", "i2"),
        rescale(
          if( i1 is null, 0, i1),
          ${td.last_results.train_min1},
          ${td.last_results.train_max1}
        ),
        rescale(
          if( i2 is null, 0, i2),
          ${td.last_results.train_min2},
          ${td.last_results.train_max2}
        )
      ) as features,
      label
    from
      samples_train
    ;

Feature vectorization for a test table can be executed in the same way.

#### Standardization

You can [standardize](https://en.wikipedia.org/wiki/Standard_score) data by using the `zscore` function. The following workflow and queries are used for standardization.

    +standardize:
      +calc_stats:
        td>: queries/calc_stats.sql
        engine: presto
        store_last_results: true
    
      +transform:
        td>: queries/transform.sql
        create_table: standardized_table

You need to calculate the mean and standard deviation for each column that you want to standardize.

    -- Presto: queires/calc_stats.sql
    select
      avg(crim) as crim_mean
      , stddev_pop(crim)  as crim_std,
      , avg(rm) as rm_mean
      , stddev_pop(rm) as rm_std
    from house_prices_train

Apply the zscore function as follows:

    -- Hive: queries/transform.sql
    select
      zscore(crim, ${td.last_resuts.crim_mean}, ${td.last_results.crim_std} as crim_scaled
      , zscore(rm, ${td.last_resuts.rm_mean}, ${td.last_results.rm_std} as rm_scaled
    from
      house_prices_train
    ;

Convert the test data set as well in the same way.

## Feature hashing and Feature Quantification

### Label encoding for categorical variables

Hivemall's feature representation is a very flexible sparse format accepting string index such as `height:172.3`. A feature vector is an array of features.

    feature ::= <index>:<weight> or <index>index ::= <INT | BIGINT | TEXT>
    weight ::= <FLOAT>

Unlike other machine learning libraries (e.g., scikit-learn), you don't need to convert `height:172.3` to an integer indexed one "3:172.3" using numerical feature index for Hivemall's linear classifiers.

However, RandomForest classifier/regressor is an exception that accepts only an integer index for a feature.

    index ::= <INT | BIGINT>

The `feature_hashing` function enables you to convert string index to integer index as follows:

    select feature_hashing(array('aaa:1.0','aaa','bbb:2.0', '3:0.3'))
    
    -- ["4063537:1.0","4063537","8459207:2.0", "4331412:0.3"]

The original motivation for using the `feature_hashing` function is to restrict the size of the feature space. It also converts numerical values into other ones. For more detail of Feature Hashing, see [this document](https://en.wikipedia.org/wiki/Feature_hashing).

    -- Hive
    select
      rowid,
      survived,
      feature_hashing(
        pclass, sex, age, sibsp, ticket, fare, cabin, embarked
      )
    from
      titanic
    ;

While `feature_hashing` is useful, it can cause hash collisions. If you want to avoid it, you can use the quantify function to assign a unique integer for each *string* feature as follows:

    -- Hive
    WITH input as (
     SELECT 'red' as fav_color, 'male' as gender, 32 as age
     UNION ALL
     SELECT 'yellow' as fav_color, 'male' as gender, 39 as age
     UNION ALL SELECT 'red' as fav_color, 'female' as gender, 19 as age
    )
    SELECT
     t1.*,
     t2.*
    FROM
     input t1
     LATERAL VIEW quantify(true, fav_color, gender, age, cast(age as string)) t2
       as fav_color_, gender_, age_, age2_

|fav_color|gender|age|fav_color_|gender_|age_|age2_|
|---|---|---:|---:|---:|---:|---:|
|red|	male|	32|	0|	0|	32|	0|
|yellow|	male|	39|	1|	0|	39|	1|
|red|	female|	19|	0|	1|	19|	2|

Here is a more practical example of applying quantification.

    -- Hive: queries/quantify_train.sql
    select
      rowid,
      survived,
      quantify(true,
        pclass, sex, age, sibsp, ticket, fare, cabin, embarked
      ) as (pclass, sex, age, sibsp, ticket, fare, cabin, embarked)
    from
      titanic_train ;

The first argument of the `quantify` function is a flag for the output result. If you want to quantify test data, you can execute as follows:

    -- Hive: queries/quantify_test.sql
    select
      rowid, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked, boat, body, home_dest
    from (
      select    rowid,    survived,
        quantify(output_row,
          pclass, sex, age, sibsp, ticket, fare, cabin, embarked
        ) as (pclass, sex, age, sibsp, ticket, fare, cabin, embarked)
      from (
        select * from (
          select
            1 as train_first -- Ensure order train data first to calculate mapping table for training data
            , false as output_row -- To recalculate mapping table with training data
            , rowid, survived, pclass, sex, age, sibsp, ticket, fare, cabin, embarked
          from
            titanic_train
          union all
          select
            2 as train_first
            , true as output_row -- To show label encoded test data
            , rowid, survived, pclass, sex, age, sibsp, ticket, fare, cabin, embarked
          from
            titanic_test
        ) t0
        order by train_first, id asc
      ) t1
    ) t2
    ;

You need to provide training data for consistent quantification between the training dataset and the test dataset.

See also:

- [Feature Hashing](https://hivemall.incubator.apache.org/userguide/ft_engineering/hashing.html)
- [Quantify non-number features](https://hivemall.incubator.apache.org/userguide/ft_engineering/quantify.html)

## Missing value imputation: How to handle missing data

Real-world data could often have missing values. Missing values could make prediction accuracy worse.

There are several strategies for handling missing values. One way is to impute data for the `NULL` value, which means to replace missing data with substituted values.

### Categorical data

The simplest way to handle missing data in a categorical feature is replacing `NULL` in the string with a value representing the missing data like `"NA"`, `"Unknown"`, and `"missing"`.

    -- Presto
    select
      coalesce(nullable_category, "Unknown")
    from
      source
    ;

### Continuous data

The easiest way to impute continuous data is to replace with the specific value like `0`.

    -- Presto
    select
      coalesce(nullable_numeric, 0.0)
    from
      source
    ;

Other strategies can be to replace the values with the overall mean, median. This example SQL replaces `0.0` in `age` column with average.

    -- Presto
    select
      if(age = 0.0, avg(age) over (), age) as age_with_mean
      ,if(age = 0.0, approx_percentile(age, 0.5) over (), age) as age_with_median
    from
      titanic
    ;

If you want to impute time series data, `lag` or `lead` functions is useful.

    -- Prestoselect
      amount
      -- Fill with previous amount value
      , if(amount = 0.0, lag(amount, 1) over (order by time), amount) as amount_lag
      -- Fill with following amount value
      , if(amount = 0.0, lead(amount, 1) over (order by time), amount) as amount_lead
    from
      sales
    ;

Find more about imputation in [this article](https://en.wikipedia.org/wiki/Imputation_(statistics)).

## Other features

Here is the list of other feature engineering functions in Hivemall document.

- [Feature interaction](https://hivemall.incubator.apache.org/userguide/ft_engineering/polynomial.htmlhttps://hivemall.incubator.apache.org/userguide/ft_engineering/polynomial.html)
    - Transforming with feature interaction, you can apply linear models with feature interactions. Hivemall provides Polynomial and Powered features.
- [Feature Binning](https://hivemall.incubator.apache.org/userguide/ft_engineering/binning.html)
    - If you want to convert numerical values into categorical values, you can use fixed-width binning. Hivemall provides `build_bins` and `feature_binning` functions for it.
- [Feature Selection](https://hivemall.incubator.apache.org/userguide/ft_engineering/selection.html)
    - In some cases, selecting important features enables you to get accurate models. You can use `select_k_best` function.
- [tf-idf](https://hivemall.incubator.apache.org/userguide/ft_engineering/tfidf.html) [[workflow example](https://github.com/treasure-data/treasure-boxes/tree/master/machine-learning-box/tf-idf)]
    - [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a well-known technique to assign the importance of terms in documents. You can extract important words with Hivemall.

## Parameter tuning

Parameter tuning is an important step in machine learning to find a better prediction model.

This section shows how to run a grid search and random search.

### Grid search

`for_each>` operator enables you to run a grid search with TD Workflow. Here we will use grid search for linear regression as an example.

In this example, we assume you want to search for two hyperparameters: `eta0` and `reg`.

    for_each>:
      eta0: [5.0, 1.0, 0.5, 0.1, 0.05, 0.01, 0.001]
      reg: ['no', 'rda', 'l1', 'l2', 'elasticnet']

You can train and evaluate as shown in the following.

    _parallel: true
    
    _do:
      _export:
        suffix: _${reg}_${eta0.toString().replace('.', '_')}
    
      +train:
        td>: queries/tarin_regressor.sql	
        create_table: regressor${suffix}
    
      +evaluate:
        td>: queries/evaluate_params.sql
        insert_into: accuracy_test

An example query for training a regressor can be written as shown in the following.

    -- Hive: queries/train_regressor.sqlselect
      train_regressor(
        add_bias(features)
        ,price
        ,'--loss_function squaredloss --optimizer adagrad -eta0 ${eta0} -iter ${iter} -reg ${reg}'
      )
    from
      train
    ;

You can write an evaluation query for regressors with `suffix` as shown in the following.

    -- Hive: queries/evaluate_params.sql
    with features_exploded as (
      select
        h.rowid
        ,extract_feature(t.fv) as feature
        ,extract_weight(t.fv) as value
      from
        test h
        LATERAL VIEW explode(add_bias(features)) t as fv
    ),
    prediction as (
      select
        t1.price as actual_price,
        t2.predicted_price
      from
        test t1
      join (
        select
          t1.rowid
          ,sum(m.weight * t1.value) as predicted_price
        from
          features_exploded t1
          LEFT OUTER JOIN regressor${suffix} m ON (t1.feature = m.feature)
        group by
          t1.rowid
      ) t2
      on t1.rowid = t2.rowid
    )
    -- DIGDAG_INSERT_LINE
    select
      rmse(predicted_price, actual_price) as rmse
      ,mae(predicted_price, actual_price) as mae
      , cast(${eta0} as double) as eta0
      , "${reg}" as reg
    from
      prediction p
    ;

This query inserts RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error), measurements for regression, to find the best parameters.

Now, you can find the best model by using the following workflow.

    +persist_best:
      +choose_best:
        td>: queries/best_param.sql
        engine: presto
        measure: rmse
        store_last_results: true
    
      +save_model:
        td_ddl>:
        suffix: _${td.last_results.reg}_${td.last_results.eta0.toString().replace('.', '_')}
        rename_tables: [{from: "regressor${suffix}", to: regressor_best}]

    -- Presto: queries/best_param.sql
    select
      *
    from
      accuracy_test
    order by
      ${measure}
    limit 1
    ;

Finally, `+save_model` task saves the best model as `regressor_best` table.

Here is the whole workflow for a grid search. This workflow and the queries can be found at the [workflow-examples repository](https://github.com/treasure-data/workflow-examples/blob/master/machine-learning/house_price/search_hyperparams.dig).

    +parameter_tuning:
      for_each>:
        eta0: [5.0, 1.0, 0.5, 0.1, 0.05, 0.01, 0.001]
        reg: ['no', 'rda', 'l1', 'l2', 'elasticnet']
    
      _parallel: true
    
      _do:
        +train:
          td>: queries/train_regressor.sql
          suffix: _${reg}_${eta0.toString().replace('.', '_')}
          create_table: regressor${suffix}
    
        +evaluate:
          td>: queries/evaluate_params.sql
          insert_into: accuracy_test
          suffix: _${reg}_${eta0.toString().replace('.', '_')}
    
    +parsist_best:
      +choose_best:
        td>: queries/best_param.sql
        engine: presto
        measure: rmse
        store_last_results: true
    
      +show_accuracy:
        echo>: "Best model reg: ${td.last_results.reg}, eta0: ${td.last_results.eta0} RMSE: ${td.last_results.rmse}, MAE: ${td.last_results.mae}"
    
      +save_model:
        td_ddl>:
        suffix: _${td.last_results.reg}_${td.last_results.eta0.toString().replace('.', '_')}
        rename_tables: [{from: "regressor${suffix}", to: regressor_best}]
    
      +clean_up:
        for_each>:
          eta0: [5.0, 1.0, 0.5, 0.1, 0.05, 0.01, 0.001]
          reg: ['no', 'rda', 'l1', 'l2', 'elasticnet']
    
        _parallel: true
    
        _do:
          +drop_table:
            td_ddl>:
            suffix: _${reg}_${eta0.toString().replace('.', '_')}
            drop_tables: ["regressor${suffix}"]

### Random search

[Random search](https://en.wikipedia.org/wiki/Random_search) is also known as [an option for hyperparameter search](http://www.jmlr.org/papers/v13/bergstra12a.html). You can run a random search with `py>` operator as follows:

    # random_search.dig
    +generate_param_list:
      py>: rand.rand_params
      n_iter: 20 # Iteration number for parameter search
      eta0: [5.0, 1.0, 0.5, 0.1, 0.05, 0.01, 0.001]
      reg: ['no', 'rda', 'l1', 'l2', 'elasticnet']
    
    +parameter_tuning:
      for_each>:
        param: ${param_list}
    
      _parallel: true
    
      _do:
        +train:
          td>: queries/train_regressor.sql
          suffix: _${param.reg}_${param.eta0.replace('.', '_')}
          create_table: regressor${suffix}
    
        +evaluate:
          td>: queries/evaluate_params.sql
          insert_into: accuracy_test
          suffix: _${param.reg}_${param.eta0.replace('.', '_')}

The following Python script generates a parameter list. Before running this code, ensure installing scikit-learn with `pip install scikit-learn`.

    # rand.py
    def rand_params(n_iter, eta0, reg):
        from sklearn.model_selection import ParameterSampler
    
        param_dist = {"eta0": eta0, "reg": reg}
    
        param_list = list(ParameterSampler(param_dist, n_iter=n_iter))
        try:
            import digdag
            digdag.env.store({"param_list": param_list})
    
        except ImportError:
            pass
    
        return True

If you want to generate random numbers under certain distribution, you can use `scipy.stats`. You need to install scipy via `pip install scipy` as well.

    # rand.py
    def rand_params(n_iter):
        from sklearn.model_selection import ParameterSampler
        from scipy.stats import randint as sp_randint
    
        param_dist = {"max_depth": [3, None],
                  "max_features": sp_randint(1, 11),
                  "min_samples_split": sp_randint(2, 11),
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}
    
        param_list = list(ParameterSampler(param_dist, n_iter=n_iter))
        try:
            import digdag
            digdag.env.store({"param_list": param_list})
    
        except ImportError:
            pass
    
        return True