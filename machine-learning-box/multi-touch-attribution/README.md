
Data-Driven Multi-Touch Attribution
===

This Box provides a data-driven, machine learning-based templatized solution for **[Multi-Touch Attribution](https://en.wikipedia.org/wiki/Attribution_(marketing))** (**MTA**), running on your pageview data stored in Treasure Data. 

Unlike traditional rule-based MTA solutions, our template takes an advanced machine learning-based approach to accurately model customer's path to conversion and understand better about how/why marketing touchpoints bring your customer to the goal. Eventually, the insights enable you to effectively and efficiently optimize the marketing campaigns with optimal budget allocation.

The implementation is based on a [state-of-the-art academic paper](https://arxiv.org/abs/1902.00215), and one of the key concepts used in the technique is called the [Shapley value](https://en.wikipedia.org/wiki/Shapley_value) calculation. Overall performance of this template has been proven on the Treasure Data platform with some of our real datasets.

## Input

Assume we have two tables `pageviews_table` and `formfills_table` in a Treasure Data database, which contain raw data representing different touchpoints collected by [td-js-sdk](https://github.com/treasure-data/td-js-sdk). These tables respectively contain non-conversion and conversion events.

`pageviews_table`:

| `time` | `canonical_id` | `td_url` | `td_referrer` | ... | `channel_id_rec` | `channels` | `channel_source` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|

`formfills_table`:

| `time` | `canonical_id` | `td_url` | `td_referrer` | ... | `channel_id_rec` | `form_id` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|



## Workflow

```sh
$ td wf push mta # push workflow to TD
$ td wf start mta mta_shapley --session now -p td_api_key=${YOUR_TD_API_KEY}
```


## Output


## How this workflow works

For further reading for algorithm and/or workflow details, refer [this page](./docs/more.md).

## Want to learn more & try on your data?

As the sample configuration and public documentation above show, the model is fully customizable for your data depending on your own definition of conversion. Contact your Customer Success Representative if you are interested in building and testing the advanced MTA solution.