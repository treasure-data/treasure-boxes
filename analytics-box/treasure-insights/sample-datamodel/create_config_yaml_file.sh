#!/bin/bash
#! /usr/bin/env bash

echo What is the Database Name?
read databasename
echo What is the Table Name?
read tablename
echo What is the Data Model Name?
read dmname
echo What is the api_key?
read api_key

echo "tinsights create_yaml --name="${dmname}" --share_all=True --database_tables="[${databasename}/${tablename}]" --api_key="${api_key}""

databasename=${databasename}
tablename=${tablename}

COMMAND="tinsights create_yaml --name=${dmname} --share_all=True --database_tables=['"${databasename}/${tablename}"'] --api_key=${api_key}"


echo "Execute the following command to create a YAML file:"
echo
echo "    \$ $COMMAND"
echo
echo -n "Answer 'yes' or 'no': "

read REPLY
if [[ $REPLY == "yes" ]]; then
    $COMMAND
else
    echo Aborted
    exit 0
fi


endpoint=https://api.treasuredata.com
yamlfilename=datamodel_${dmname}.yaml

export dmname=${dmname}
export api_key="${api_key}"
export endpoint="${endpoint}"

echo 
echo "Copy and run following command to create a Data Model called ${dmname}..."

echo


echo 'curl -X POST --data-urlencode "yaml=$(cat datamodel_${dmname}.yaml)" -H Authorization: TD1 ${api_key} ${endpoint}/reporting/datamodels'

bash -i
