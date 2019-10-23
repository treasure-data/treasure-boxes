# Workflow definition to integrate Yahoo DMP
# Requirement
set up Treasure Data Toolbelt: Command-line Interface (https://support.treasuredata.com/hc/en-us/articles/360000720048-Treasure-Data-Toolbelt-Command-line-Interface)

# Installation (Setup)
Download this workflow.

### define workflow
Copy script of 'call_yahoo_dmp_api.dig' into `Workflow Definition` tab.
Then replace some placeholder to your own.
- ${secret:td.apikey}
- YOUR_SITE_IDZ
- YOUR_COOKIE_PARAM
- YOUR_DATABASE

### define SQL to collect user data
Declare SQL statement to retrieve user list that you want to send YahooDMP.

### push to TreasureData as Workflow project
Push it to your TD environment,
```
$ td wf push yahoo-dmp
```

# Mechanism
![Yahoo DMP integration concept](https://user-images.githubusercontent.com/248312/63661711-ab388100-c7f6-11e9-8a27-2a56e206362f.jpg)
