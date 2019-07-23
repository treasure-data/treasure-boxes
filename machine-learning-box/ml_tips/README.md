# ML tips workflow

This workflow aims to explain common ML techniques using Hivemall and Treasure Workflow.

Using [titanic data](https://github.com/amueller/scipy-2017-sklearn/blob/master/notebooks/datasets/titanic3.csv), this workflow explains the following basic techniques.

- Random/stratified splitting for train and test data
- Feature normalization
- Missing value imputation

You can see detailed document in [more.md](docs/more.md).

## Input

This workflow assumes a table as follows:

|pclass<br/>`int`|survived<br/>`int`|name<br/>`string`|sex<br/>`string`|age<br/>`int`|sibsp<br/>`int`|parch<br/>`int`|ticket<br/>`string`|fare<br/>`double`|cabin<br/>`string`|embarked<br/>`string`|boat<br/>`string`|body<br/>`int`|home.dest<br/>`string`|
|---------|------|---------|--------|-------|-------|-------|--------|-------|-------|-----------|--------|---------|-------|
|1|1|"Allen, Miss. Elisabeth Walton"|female|29|0|0|24160|211.3375|B5|S|2||"St Louis, MO"|
|1|1|"Allison, Master. Hudson Trevor"|male|0.9167|1|2|113781|151.5500|C22 C26|S|11||"Montreal, PQ / Chesterville, ON"|
|1|0|"Allison, Miss. Helen Loraine"|female|2|1|2|113781|151.5500|C22 C26|S|||"Montreal, PQ / Chesterville, ON"|
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|

Here is a description of each column.

    pclass          Passenger Class
                    (1 = 1st; 2 = 2nd; 3 = 3rd)
    survival        Survival
                    (0 = No; 1 = Yes)
    name            Name
    sex             Sex
    age             Age
    sibsp           Number of Siblings/Spouses Aboard
    parch           Number of Parents/Children Aboard
    ticket          Ticket Number
    fare            Passenger Fare
    cabin           Cabin
    embarked        Port of Embarkation
                    (C = Cherbourg; Q = Queenstown; S = Southampton)
    boat            Lifeboat
    body            Body Identification Number
    home.dest       Home/Destination

In this workflow, you will predict the probability of `survival`, taking a binary label survival as a response variable.

## Workflow

```sh
$ ./data.sh # Upload sample dataset to Treasure Data
$ td wf push ml_tips
$ td wf start ml_tips titanic --session now
```

- [titanic.dig](titanic.dig) - TD workflow script for linear classifier with Hinge Loss and Random Forest classifier in parallel.

### Note for Random Forest classifier

As of Hivemall v0.5.2, there is [a performance issue](https://issues.apache.org/jira/projects/HIVEMALL/issues/HIVEMALL-243) around Random Forest classifier with feature hashing for nominal features. To avoid it, a workaround is implemented in the workflow to limit the feature hashing space with using cardinality of the categorical feature.

## Output

This workflow outputs the probability of surviving as follows:

| rowid<br/>`string` | probability<br/>`double` |
|:---:|:---|
| 1-10 |0.23813835|
| 1-1001 |0.6909432|
| ... |...|

AUC and Log Loss on a workflow log as follows:

```
echo>: auc: 0.8044451551007356    logloss: 0.5337748192743182
```

## Conclusion

Treasure Workflow and Hivemall provide an easy way for feature engineerings such as feature scaling and missing value imputation.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).
