# Workflow: Scenario (compare tasks's duration in workflow between multiple attempts)

## Scenario

The purpose of  this scenario is to compare tasks's duration in workflow between multiple attemps.

### Steps
#### 1. push this workflow to Treasure Data
```
> cd compare_workflow_task
> td push compare_workflow_task
```

#### 2. configure endpoint settings
  - api_endpoint
  - workflow_endpoint
![](images/1.png)

#### 3. configure attempts (you want to compare attempt)
![](images/2.png)

#### 4. register td.apikey as a secret (Owner of td.apikey must be attempts which you specify.)
![](images/3.png)

#### 5. run workflow
![](images/4.png)


After this workflow run, you can get the following query result.
![](images/5.png)

![](images/6.png)

You can compare tasks's duration between multiple attempts.