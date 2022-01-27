# Integration of DialogOne with Treasure Data 
DialogOne is a service that automatically links DAC’s DialogOne with CDPs (customer data platform) and other databases owned by companies. With this service, companies can seamlessly integrate their own data with LINE Official Account action data acquired by DialogOne for marketing purposes.
And this workflow helps you to post the segment users' list to DialogOne for messaging on LINE.

# Prerequisite
- Following parameters are necessary.

| Variable | Description | Example | provided by |
| -------- | ----------- | -------- | -------- |
| acid | Account identifier. | `abcdef123456789a`| DAC |
| sa_email | Email address for service account. | `example@test-project.iam.gserviceaccount.com`| DAC |
| private_key | Private key for service account. | `-----BEGIN PRIVATE KEY-----\nABCDEFGHIJKLMNOPQRSTUVWXYZ......abcdefghijklmnopqrstuvwxyz+1234567890=\n-----END PRIVATE KEY-----\n`| DAC |
| private_key_id | Private key ID for service account. | `abcdef123456789abcdef123456789abcdef1234`| DAC |
| td.apikey | **Master** API Key. [link](https://docs.treasuredata.com/display/public/PD/Getting+Your+API+Keys) | `1234/abcdefghijklmnopqrstuvwxyz1234567890`| Treasure Data |
| database | Name of database has a table for user IDs. | `sample_database` | Treasure Data |
| filename | Name of output CSV file you want to set. (*less than 255 characters and use only alphanumeric characters, numbers, underscores, dots, and hyphens.) | `output_user_list`|  |
| sqlfile | Name of file contains SQL to retrieve user IDs. | `user_id_list.sql` |  |

# SQL query
Set only one column for LINE user ID in the query like below.
※LINE user ID: a string matches the regex pattern `U[0-9a-f]{32}`

`user_id_list.sql`
```
SELECT 
  user_id
FROM
  sample_db.sample_table
```

# About uploaded file
When you upload the same name file as you have uploaded before, the older file replaces the newer one.
A file uploaded / updated expires in 30 days.

# Installation (TD Toolbelt)  
### 1. Prepare the files to upload.
After downloading and decompressing the file, place a SQL file contains query to retrieve user IDs in the directory.
You can change the name of the Digdag file (.dig) that will be workflow project name if you want. But don't rename the Python file (.py)

Open the Digdag file and update the values of the variables except `td.apikey`, `private_key` and `private_key_id`.

### 2. Upload files to Treasure Data.
Move to the directory includes the Digdag file and excute the command below.

    $ td wf push [Digdag file name]
### 3. Set Secrets.
Set the values of [Secrets](https://docs.treasuredata.com/display/public/PD/About+Workflow+Secret+Management).
`private_key` is too long value to set and we recommend you to make it a text file then set it like below. (Be careful not to upload the key file!)

    $ td wf secrets --project [Digdag file name] --set td.apikey
    $ td wf secrets --project [Digdag file name] --set private_key=@private_key.txt
    $ td wf secrets --project [Digdag file name] --set private_key_id


# Further Reading
- TD Toolbelt
https://docs.treasuredata.com/display/public/PD/Treasure+Workflow+Quick+Start+using+TD+Toolbelt+in+a+CLI
- pytd
https://github.com/treasure-data/pytd

