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

echo -e "userid\tpost\tage\tgender" > blogposts.tsv
jq -r -c '.[] | [.post,.age,.gender] | @tsv' train.json | awk '{print NR"\t"$0}' >> blogposts.tsv
jq -r -c '.[] | [.post,.age,.gender] | @tsv' test.json | awk '{print 526812+NR"\t"$0}' >> blogposts.tsv
```

## Import data to Treasure Data

Please import prepared blog post data to Treasure Data as follows:

```sh
# create database
td db:create td_test

# load training data
td table:create td_test blogposts
td import:auto --auto-create td_test.blogposts --format tsv --column-header --time-value `date +%s` --column-types "int,string,int,string" ./blogposts.tsv
```

# Run gender-age prediction workflow

```sh
# Push workflows to Treasure workflow
$ td wf push td_test

# Run workflow from command line (also runnable from GUI)
$ td wf run blogposts.dig
```