# Treasure Insights - Sample ShellScript to Create DataModel

You can build Treasure Insight dashboard using API

## Requirement

* Treasure Insight License
* Treasure Insights Dashboard Access
* TD API Key
* Treasure Insights Sharing Users
* TD Database name
* TD Table name

# Step

1. Prepare a configuration file for Data Model
2. Run create_config_yaml_file.sh `$ ./create_config_yaml_file.sh`
Creates the config Yaml file
3. Copy the Curl command from the raw output
4. Run curl command to create a data model

Ex: 'curl -X POST --data-urlencode "yaml=$(cat datamodel_${dmname}.yaml)" -H Authorization: TD1 ${api_key} ${endpoint}/reporting/datamodels'





