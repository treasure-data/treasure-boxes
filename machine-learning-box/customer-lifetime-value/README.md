Customer Lifetime Value Prediction Template
===

Predicting Customer Lifetime Value (CLTV) allows you to efficiently identify high-value customers and understand their characteristics. Eventually, you can effectively optimize your day-to-day marketing activities without missing important highly-engaged customers.

## Input

*Data source: [UCI Machine Learning Repository: Online Retail Data Set](http://archive.ics.uci.edu/ml/datasets/Online+Retail).*

As an online retailer, assume we have [a `source` table](./config/general.yml#L3) that represents customer's order histories as follows:

| InvoiceNo<br/>`string` | InvoiceDate<br/>`string` | CustomerID<br/>`long` | Country<br/>`string` | StockCode<br/>`string` | Description<br/>`string` | UnitPrice <br/>`double` | Quantity<br/>`long` | 
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 536365 | 2010/12/01 8:26 | 17850 | United Kingdom | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 2.55 | 6 |
| 536365 | 2010/12/01 8:26 | 17850 | United Kingdom | 71053 | WHITE METAL LANTERN | 3.39 | 6 |
| 536365 | 2010/12/01 8:26 | 17850 | United Kingdom | 84406B | CREAM CUPID HEARTS COAT HANGER | 2.75 | 8 |
| ... |...|...| ...|...|...|...|...|
| C536391 | 2010/12/01 10:24 | 17548 | United Kingdom | 22556 | PLASTERS IN TIN CIRCUS PARADE  | 1.65 | -12 |
| ... |...|...| ...|...|...|...|...|

Here, each row represents single item (i.e., **StockCode**) in a basket corresponding to single order (i.e., **InvoiceNo**). That is, a CLTV can be calculated by **a sum of (UnitPrice * Quantity)** for unique CustomerID.

> **Note:** Negative **Quantity** represents returned items.

## Workflow

Set your database and table name to [`config/general.yml`](./config/general.yml).

Run a ready-made workflow template for CLTV prediction:

```sh
$ td wf push cltv-prediction # push workflow to TD
$ td wf secrets --project cltv-prediction --set td.apikey td.apiserver
$ td wf start cltv-prediction predict --session now 
```

|Variable|Description|Example|
|:---|:---|:---|
|`td.apikey`|TD API key to be used in the script. Access Type must be `Master Key`.|`1234/abcdefghijklmnopqrstuvwxyz1234567890`|
|`td.apiserver`|TD API endpoint starting with `https://`.|`https://api.treasuredata.com`|

In the middle of the workflow, we import the [Online Retail Data Set](http://archive.ics.uci.edu/ml/datasets/Online+Retail) to a table, calculate CLTV for every single **CustomerID**, and enrich their attributes with basic statistics:

| customerid<br/>`long` | cltv<br/>`double` | country<br/>`string` | recency<br/>`long` | avg_basket_value<br/>`double` | avg_basket_size<br/>`long` | cnt_returns<br/>`long` | has_returned<br/>`boolean` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 14001 | 2030.33 | United Kingdom | 327 | 681.0266666666666 | 320.6666666666667 | 1 | 1 |
| 14911 | 132572.6200000001 |  EIRE | 372 | 715.5475621890546 | 400.5721393034826 | 47 | 1 |
| 18144 | 2888.7499999999995 | United Kingdom | 365 | 240.72916666666666 | 111.91666666666667 | 0 | 0 |
| ... |...|...| ...|...|...|...|...|

A derived attribute `recency` is the number of days between the first order and last order. 

## Output

The output of workflow is a table that contains predicted CLTV for a subset of customers:

| customerid<br/>`long` | predicted_cltv<br/>`double` |
|:---:|:---:|
|12355|68.84149528775471|
|12356|172.29478943269208|
|12357|151.84542283221555|
| ... | ... |

Meanwhile, the Workflow execution log tells you the accuracy of prediction:

```
Accuracy RMSE: 4623.584016620842, MAE: 1777.0782472268297
```

It's time to tweak your model with custom hyper-parameters in [`queries/train_regressor.sql`](./queries/train_regressor.sql). Notice that this template uses a linear regressor to make CLTV prediction.

## Reference

- [Predicting Customer Lifetime Value with AI Platform: training the models](https://cloud.google.com/solutions/machine-learning/clv-prediction-with-offline-training-train)
