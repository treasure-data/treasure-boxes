TF-IDF Template
===

**TF-IDF** is a composite weight for each word in each document.  

This page introduces a workflow template to calculate TF-IDF and to get top-k important keywords in each document. You can easily build a TF-IDF workflow following this guide.  

## Input

This workflow takes a table of the following form:

| docid<br/>`long` | contents<br/>`string` |
|---:|:---:|
|1|Justice, in its broadest context,...|
|2|Wisdom (sophia) is the ability to think ...|
| ... |...|

## Workflow

We prepared a basic workflow for TF-IDF calculation and getting top-k important keywords in each document.  

```sh
$ sh sh/data.sh # prepare sample dataset
$ sh sh/stopwords.sh # prepare stopwords table
$ td wf push tfidf # push workflow to TD
$ td wf start tfidf tfidf --session now -p apikey=${YOUR_TD_API_KEY}
```

* [tfidf.dig](tfidf.dig) - TD workflow script for [TF-IDF](https://github.com/myui/hivemall/wiki/TFIDF-calculation) calculation and getting top-k important keywords in each document.
* [config/params.yml](config/params.yml) - defines configurable parameters for the TF-IDF workflow such as `k` of top-k (default: 3),language of the documents (english/japanese, default: english).

**Caution:** This workflow presupposes the existence of stopwords table. You need to excute [sh/stopwords.sh](sh/stopwords.sh) to create stopwords table, or if you use your own stopwords table, you should rewrite the parameter of [config/params.yml](config/params.yml).

**Note:** `stopwords` are words such as _the,is,at,which_. These are filtered out before or after processing of natural language data.

## Output

The outputs of workflow are two tables.  

One is a table that a list of words and TF-IDF for each document as shown below:

| docid<br/>`long` | tfidf<br/>`array<string>` |
|:---:|:---:|
| 1 |["justice:0.1758477689430746","based:0.07033910867777095",...]|
| 2 |["action:0.08688948589543341","wisdom:0.06516711579725143",...]|
| ... |...|

Another is a table that contains a list of important keywords for each document as shown below:

| docid<br/>`long` | keywords<br/>`array<string>` |
|:---:|:---|
| 1 |["philosophy","study"]|
| 2 |["experience","knowledge","understanding"]|
| ... |...|

**Note:** Because of sample dataset has only 3 documents and the query to get top-k kewords in this workflow use words at least two occourence in documents, the first row of the output table has only 2 words. 

## How This Workflow Works

For further reading for algorithm and/or workflow details, please refer [this page](docs/more.md). 