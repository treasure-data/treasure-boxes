# Workflow Visualizer - Experimental

Workflow Visualizer is a simple tool to visualize Treasure Workflow task dependency.

![](https://t.gyazo.com/teams/treasure-data/c1ea9afc1565f0c23ce1e9036a5d88e1.png)

## How to use workflow visualizer

### 1. Download tasks

Use `curl` command as following and save the results as "tasks.json":

```
    $ export TD_API_KEY=<your api key>
    $ export ATTEMPT_ID=<attempt id>
    $ curl -H "Authorization: TD1 $TD_API_KEY" https://api-workflow.treasuredata.com/api/attempts/$ATTEMPT_ID/tasks -o tasks.json
```

* "tasks.json" file must be on the same directory with index.html, all.json, and style.css.
* You can find ATTEMPT_ID at the "ATTEMPT HISTORY" tab of "Run History" page on our workflow console. Number at the URL is not attempt id (it's a session id).



### 2. Start HTTP server

Run this command to start a http server:

    $ python -m SimpleHTTPServer 8000

If it fails (python version 3 has different command), use this command instead:

    $ python -m http.server 8000


### 3. Open it

Open http://localhost:8000/index.html using your browser.

## Demo

1. Access to [demo app](https://demo-treasureworkflow-visualizer.s3.amazonaws.com/index.html)
2. Input your endpoint / master apikey / attempt id
3. Click Visualize

NOTE: APIKEY is used in url parameter in the demo app. Generate a temp master apikey. After you test it, recommend to erase the apikey.
