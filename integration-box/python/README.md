# Getting Started with Python Custom Scripting

## What is Python Custom Scripting?

Python scripts can be run from [TD workflow][workflow] or [Digdag][digdag], using the Python operator `py>`. The workflow itself can be created via Treasure Data Console and/or the CLI. In the workflow, specify a Docker image to use for running the Python script. When the workflow task starts, a new Docker container is created based on the specified docker image. Then, the Python script is executed in the container in an isolated environment.

# Prerequisites

* Download [td cli][td]. This allows the user to manage workflows from command line.
* During alpha and beta `Python 3.6.8` and `Anaconda3 5.3.0` are supported. Hence, your Python code must be compatible with either one.
* Basic Knowledge of Treasure Workflow's [syntax][wf syntax]

Optionally, some users might find [this wrapper for td cli useful][tdwf]. If you want to use it, run:

```bash
curl -sL https://gist.github.com/kiyoto/d46ccf71faa924320c0a7993515d0e9c > /usr/local/bin/tdwf
chmod +x /usr/local/bin/tdwf
```

# Simple Python Functions

This directory contains simple examples such as:

- How to call functions
- How to pass parameters to functions
- How to use environment variables
- How to import functions

## How to Run This Example

You can copy this directory (or clone the entire repository and navigate to this one).

To know that you are in the right place, type `ls` in the terminal and you should see the following.

```
$ ls
README.md	other_scripts	scripts		simple.dig
```

Then, you can push it to Treasure Data via `td wf push` as follows.

```
$ td wf push simple-example
2019-05-13 21:01:31 -0700: Digdag v0.9.36
Creating .digdag/tmp/archive-6767391817040041451.tar.gz...
  Archiving other_scripts/__init__.py
  Archiving simple.dig
  Archiving README.md
  Archiving py_scripts/examples.py
Workflows:
  simple.dig
Uploaded:
  id: 24510
  name: simple-example
  revision: efcd18bf-1435-4518-bbea-60ac445e861d
  archive type: s3
  project created at: 2019-05-14T04:00:10Z
  revision updated at: 2019-05-14T04:01:34Z

Use `td workflow workflows` to show all workflows.
```

Then, go to your Treasure Data instance and you can see your workflow uploaded. Note that `td wf push` accepts a parameter `--revision` which can be used to set your own revision ID, such as commit hash, your internal release versions, etc.

To run the workflow, run

```
$ td wf start simple-example simple --session now
2019-05-13 21:04:32 -0700: Digdag v0.9.36
Started a session attempt:
  session id: 250802
  attempt id: 250930
  uuid: 2453cfa8-2b16-4a6f-83c2-9e9c9e7cdb33
  project: simple-example
  workflow: simple
  session time: 2019-05-14 04:04:32 +0000
  retry attempt name: 
  params: {}
  created at: 2019-05-13 21:04:35 -0700

* Use `td workflow session 250802` to show session status.
* Use `td workflow task 250930` and `td workflow log 250930` to show task status and logs.
```

You can see your workflow result in the console. Alternatively, you can see them via `td wf log/task/session` commands as shown in the execution log of `td wf start`

## Further Readings

- [py> operator documentation](https://docs.digdag.io/operators/py.html)
- [Pandas DataFrame examples](../pandas-df)
