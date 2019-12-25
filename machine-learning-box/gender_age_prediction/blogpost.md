Please download dataset from [Kaggle](https://www.kaggle.com/tomlisankie/blog-posts-labeled-with-age-and-gender/download) first. 

Then, you need a Kaggle account for download. Please set your kaggle API credentials in ~/.kaggle/kaggle.json following [this instruction](https://github.com/Kaggle/kaggle-api#api-credentials).

## Prepare data

Please download dataset from kaggle and run the following data preprocessing.


```sh
pip install kaggle

chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download tomlisankie/blog-posts-labeled-with-age-and-gender

unzip blog-posts-labeled-with-age-and-gender.zip 

brew install jq

echo -e "userid\tpost\tage\tgender" > train.tsv
jq -r -c '.[] | [.post,.age,.gender] | @tsv' train.json | awk '{print NR"\t"$0}' >> train.tsv

echo -e "userid\tpost\tage\tgender" > test.tsv
jq -r -c '.[] | [.post,.age,.gender] | @tsv' test.json | awk '{print 526812+NR"\t"$0}' >> test.tsv
```

## Import data to Treasure Data

Please import prepared blog post data to Treasure Data as follows:

```sh
# create database
td db:create blogposts

# load training data
td table:create blogposts train
td import:auto --auto-create blogposts.train --format tsv --column-header --time-value `date +%s` --column-types "int,string,int,string" ./train.tsv

# load test data
td table:create blogposts test
td import:auto --auto-create blogposts.test --format tsv --column-header --time-value `date +%s` --column-types "int,string,int,string" ./test.tsv
```