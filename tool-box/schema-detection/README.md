# Source level schema detection
With evolution of cloud storage and every changing application handling schema changes is a critical part of any application. Ensuring that our customers can bring data of any shape, size, type on our Customer Data Platform is the most critical requirement for us. In this example, we have created a workflow which will handle schema change at the source at run time.

# Getting started
1. Download the folder locally
2. Use [TD Toolbelt](https://support.treasuredata.com/hc/en-us/articles/360001262207) to upload this folder as a Treasure Workflow project into your Treasure data account
3. Provide a yaml file with input file and output database in treasure data information
4. Provide database name and apikey as a variable in .dig file
5. Run the wf_dynamic_mapping.dig file

# How it works

Here is the breif description what each tasks do in the workflow 

1. Config-s3.yml file is provided which contains all the input and output TD database storage information ( In this example AWS s3 bucket is our source )
2. Database name and apikey information is provided as a variable into the .dig file
3. Custom python script runtime_linking.py is ran in the workflow in which config-s3.yml file is provided as a input
4. The "https://api.treasuredata.com/v3/bulk_loads/guess" post API request helps to create a guess file from the config file provided
5. The datatypes of all the columns in the guess file are converted to the string
6. When the workflow is ran for the first time the schema information is stored into a table at TD database , next time when the workflow runs it checks the number of columns present into the table and if there is a change then users are notified by a mail
7. To get the email notifications smtp connections must be set

# Output 

 Yaml file which needs to be provided 

[![config-file.png](https://i.postimg.cc/CdTVbJvb/config-file.png)](https://postimg.cc/BPgy05fv)

 Table into the treasure data platform 
 
 [![Screen-Shot-2019-09-18-at-3-47-49-PM.png](https://i.postimg.cc/gjHq6xXz/Screen-Shot-2019-09-18-at-3-47-49-PM.png)](https://postimg.cc/XBXyR7km)
 
 Addition of extra column into the table 
 
 [![Screen-Shot-2019-09-18-at-3-47-55-PM.png](https://i.postimg.cc/66M8TVT7/Screen-Shot-2019-09-18-at-3-47-55-PM.png)](https://postimg.cc/MXj6FQ7x)
 
 Email notification of any change into the schema 
 
 [![Screen-Shot-2019-09-18-at-3-58-21-PM.png](https://i.postimg.cc/DwZHnTHJ/Screen-Shot-2019-09-18-at-3-58-21-PM.png)](https://postimg.cc/VdxDW3Ym)
 
 # Questions 
 
 Please feel free to reach out to support@treasure-data.com with any questions you have about using this code for Fuzzy Matching


 


