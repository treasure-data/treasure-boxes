# Treasure Data Find Usage Tool

By passing a specific word such as table name, database name, etc. as an argument to this script and executing it, you can see which Workflows and Queries contain it.

## Prerequisites
* Python 3+
*  [Installing TD Toolbelt](https://docs.treasuredata.com/display/PD/Installing+TD+Toolbelt+and+Treasure+Agent)


## Installation

Download the file and place it in the desired location.

## How To Use

If you want to find out how much a table called **sample_table** is used in Workflow or Queries, you can run the command as follows
```
python find_usage.py samples_table
```


## Options
```
find_usage.py [-h] [-f FILE] [-t {workflow,queries,all}] keyword
```
|Short Option|Long Option|Description                                                                                                                   
|-|-|-
|-h|---help|Show details about the command.
|-f|---file|File name to output. <br>(When you use this option it will change to file output mode.)
|-t|--target|Range of targets to search.<br><br>**workflow**: Search within Workflow.<br>**queries**: Search within Queries.<br>**all**: Search them both.


## About Processing Time

This script uses the td command (TD Toolbelt) to retrieve workflow and query information, stores the results as files in a temporary folder, and returns results after searching the contents of those files.

Therefore, it may take a long time to search for workflows, depending on the number of workflows created on the treasure data.
(Even in standard use, it takes a few minute to process.)
