## How to use

Workflow example of AutoML operator. 

Note: this feature is still in Beta and available to limited customers.


```sh
# Push project
$ td -c ~/.td/td.conf wf push <project_name> --project .

# Setting td.apikey secret is required for automl operator.

$ td -c ~/.td/td.conf wf secrets --project <project_name> --set td.apikey
```