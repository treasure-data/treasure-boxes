## How to Run This Example

You can copy this directory (or clone the entire repository and navigate to this one).

To know that you are in the right place, type `ls` in the terminal and you should see the following.

```
$ ls
README.md	other_scripts	py_scripts		simple.dig
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