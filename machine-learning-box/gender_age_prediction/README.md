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
