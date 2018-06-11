LDA topic modeling template
===

This workflow shows an example how to apply [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)-based [topic modeling](https://en.wikipedia.org/wiki/Topic_model) which often be used for document clustering.

## Input

This workflow takes a table of the following form:

| docid<br/>`long` | contents `string` |
|---:|:---|
|2238|A red oak tree a few miles down the road from Terry A. Andersons ...|
|2240|A veteran jockey who had planned to retire at the end of the year ...|
|2241|The bloodiest of four army uprisings in four years was also the ...|
| ... |...|...|

You can used `$ bin/load_data.sh` to prepare the above example table on Treasure data.

## Workflow

```sh
# push workflow to TD
$ td wf push lda_wf

# run workflow
$ td wf start lda_wf lda --session now
```
  
## Output

The output of workflow consists of the following three tables:

`lda_model` table stores model parameter of LDA. `lambda` 

| label | word | lambda |
|---:|---:|---:|
| 5 | eritrean | 7.959341132846021e-07 |
| 5 | altovise | 7.959536105772713e-07 |
| 5 | governmed | 7.959557137837692e-07 |
| .. | .. | .. |

`predicted_topics` table shows assigned topic(s) for each document. 
`proba1`/`proba2` represents probability be `topic1`/`topic2`, respectively. 
`topic1` is the topic id that a document is most likely to be described. `topic2` can be null when there is no second topic candidate.

| docid | topic1 | proba1 | topic2 | proba2 |
|---:|---:|---:|---:|---:|
| 5 | 6 | 0.1428571492433548 | | |
| 6 | 0 | 0.1478169709444046 | 6 | 0.1420305073261261 |
| 7 | 6 | 0.1428571492433548 | | |
| 8 | 6 | 0.1428571492433548 | | |

`topicwords` shows topic-describing words for each topic.

| topic | words |
|:-:|:--|
| 0 | [ "museum", "art", "short", "museums", "tomb", "black", "nazi", "divorce", ... ] |
| 1 | [ "band", "recording", "poet", "album", "charles", "nea", "fulton", "rjr", ... ] |
| 2 | [ "family", "gallery", "friends", "the dog", "nixon", "art", "door", "monet", ... ] |
| 3 | [ "people", "government", "president", "officials", "police", "united", ... ] |
| 4 | [ "percent", "market", "million", "stock", "billion", "prices", "rose", ... ] |
| 5 | [ "billboard", "test", "fda", "transplant", "trailer", "patients", "surgery", ... ] |
| 6 | [ "maxwell", "shark", "randolph", "comedy", "opera", "dunn", "sang", "historic", ... ] |


## Conclusion

Treasure Workflow provides an easy way to apply document clustering using LDA. 
What you need to prepare is just an input table.

Note that you can find stopwords in various languages in [PostgreSQL repository](https://github.com/postgres/postgres/tree/master/src/backend/snowball/stopwords).
Better to replace [stopwords.csv](.resources/stopwords.csv) for non-English texts.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).
