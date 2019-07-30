# Getting Started with Python Custom Scripting

## What is Python Custom Scripting?

Python scripts can be run from [TD workflow][workflow] or [Digdag][digdag], using the Python operator `py>`. The workflow itself can be created via Treasure Data Console and/or the CLI. In the workflow, specify a Docker image to use for running the Python script. When the workflow task starts, a new Docker container is created based on the specified docker image. Then, the Python script is executed in the container in an isolated environment.

## Prerequisites

* Download [td cli][td]. This allows the user to manage workflows from command line.
* During alpha and beta `Python 3.6.8` and `Anaconda3 5.3.0` are supported. Hence, your Python code must be compatible with either one.
* Basic Knowledge of Treasure Workflow's [syntax][wf syntax]

Optionally, some users might find [this wrapper for td cli useful][tdwf]. If you want to use it, run:

```bash
curl -sL https://gist.github.com/kiyoto/d46ccf71faa924320c0a7993515d0e9c > /usr/local/bin/tdwf
chmod +x /usr/local/bin/tdwf
```

## Examples

### Simple Python Functions

See [this directory](./simple) for simple examples. These examples go through basics such as:

- How to call functions
- How to pass parameters to functions
- How to use environment variables
- How to import functions

### Reading and Writing Data from Treasure Data

The examples in [this directory](./pandas-df) shows how to read data in Treasure Data into a Dataframe, manipulate data, and write it back to Treasure Data as a table.


[workflow]: https://support.treasuredata.com/hc/en-us/articles/360001262227-Treasure-Data-Workflow-Quick-Start-in-TD-Console
[digdag]: https://digdag.io
[td]: https://toolbelt.treasuredata.com
[tdwf]: https://gist.github.com/kiyoto/d46ccf71faa924320c0a7993515d0e9c
[wf syntax]: https://support.treasuredata.com/hc/en-us/articles/360001266668-Workflows-Syntax