# Integration of DialogOne with Treasure Data 
DialogOne is a service that automatically links DAC’s DialogOne with CDPs (customer data platform) and other databases owned by companies. With this service, companies can seamlessly integrate their own data with LINE Official Account action data acquired by DialogOne for marketing purposes.
And this workflow helps you to post the segment users' list to DialogOne for messaging on LINE.

# Prerequisite
- Following parameters are necessary.

| Variable | Description | Example | provided by |
| -------- | ----------- | -------- | -------- |
| acid | Account identifier. | `abcdef123456789a`| DAC |
| api_key | API key | `a1b2c3d4-5ef6-777a-888b-9abc12ed345f`| DAC |
| service_id | Service ID. | `4`| DAC |
| td.apikey | **Master** API Key. [link](https://docs.treasuredata.com/display/public/PD/Getting+Your+API+Keys) | `1234/abcdefghijklmnopqrstuvwxyz1234567890`| Treasure Data |
| database | Name of database has a table for LINE UserIDs. | `sample_database` | Treasure Data |
| table | Name of table for LINE UserIDs. | `sample_table` | Treasure Data |
| user_id_column | Name of column for LINE UserIDs. | `user_id` | Treasure Data |

# About uploaded file
When you upload the same name file as you have uploaded before, the older file replaces the newer one.  
A file uploaded / updated expires in 30 days.

# Installation (TD Toolbelt)  
### 1. Prepare the files to upload.
After downloading and decompressing the file, upload them to Treasure Data.
You can change the name of the Digdag file (.dig) that will be workflow project name if you want. But don't rename the Python file (.py)

Open the Digdag file and update the values of the variables for `_export` part.

### 2. Upload files to Treasure Data.
Move to the directory includes the Digdag file and excute the command below.

    $ td wf push [Digdag file name]
### 3. Set Secrets.
Set the values below as [Secrets](https://docs.treasuredata.com/display/public/PD/About+Workflow+Secret+Management).
-td.apikey
-api_key (provided from DAC)
-acid (provided from DAC)
-service_id (provided from DAC)

    $ td wf secrets --project [Digdag file name] --set td.apikey
    $ td wf secrets --project [Digdag file name] --set api_key
    $ td wf secrets --project [Digdag file name] --set acid
    $ td wf secrets --project [Digdag file name] --set service_id

# Further Reading
- TD Toolbelt
https://docs.treasuredata.com/display/public/PD/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI
- pytd
https://github.com/treasure-data/pytd

