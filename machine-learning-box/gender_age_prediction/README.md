# Gender age prediction workflow

```sh
# Download gender age prediction workflow
$ https://github.com/treasure-data/treasure-boxes.git
$ cd treasure-boxes/machine-learning-box/gender_age_prediction

# Configure parameters to meet your situation
$ vi config/params.yml

# Push workflows to Treasure workflow
$ td wf push rf_test

# Run workflow from command line (also runnable from GUI)
$ td wf run rf_predict.dig
```

# Assumed input

[gender_age table](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/augment.dig#L19)

|userid|gender_age|
|:-:|:-:|
|aaa|M20|
|bbb|M35|
|ccc|F40|
|...|M60|

Any format is accepted for `userid` and `gender_age` but recommend `age_range` is increased by 5 or 10.
We assume `gender_age` is known at least for 5% users.

[features table](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/augment.dig#L37)

|userid|features|
|:-:|:-:|
|aaa|['apple:3.7','tv:3.9']|
|bbb|['tv:3.9','fashion:8.1']|
|ddd|['microsoft:1.2','apple:4.2','game:6.7']|
|...|..|

Each `features` takes a feature vector in a [Hivemall format](http://hivemall.apache.org/userguide/getting_started/input-format.html#features-format-for-classification-and-regression) (libsvm format).

# Output

[rf_complemented table](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/rf_predict.dig#L112)

|userid|gender_age|
|:-:|:-:|
|aaa|M20|
|bbb|M35|
|ccc|F40|
|ddd|M40|

Missing `gender_age` cells are filled by predicted result.

# How to use

1. Modify [config/params.yml](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/config/params.yml) to meet your setting.
2. Modify [gender_age task](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/augment.dig#L19) in augment.dig creating `gender_age` table.
3. Modify [vectorize task](https://github.com/treasure-data/treasure-boxes/blob/master/machine-learning-box/gender_age_prediction/augment.dig#L22) in augment.dig creating `features` table.
