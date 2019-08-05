# Integration of Onetrust service with Treasure Data 
OneTrust is a privacy management and marketing compliance tech company. Its services are used by 
organizations to comply global regulations like GDPR
This example shows how to connect to profiles and collection endpoints and ingest the 
data into Treasure Data. This data can be used by marketers to suppress activations based on consent 


## Push the code and set variables
```
td wf push --project onetrust_integration
td wf secret --project onetrust_integration --set onetrustapikeys.yml #create a .yml file with all the secrets and set them for the project  

```

-  Data Subject  A data subject is any person whose personal data is being collected, held or processed (https://eugdprcompliant.com/what-is-data-subject/)

- Consent The informed, unambiguous and freely given permission from the data subject to have data relating to him or her processed. 

- Refer this link for understanding key terms under GDPR (https://eugdprcompliant.com/key-terms/)


