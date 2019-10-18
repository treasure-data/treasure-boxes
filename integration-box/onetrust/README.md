# Integration of Onetrust with Treasure Data

 OneTrust is a privacy management and marketing compliance tech company. Its services are used by organizations to comply global regulations like GDPR.
 Refer the below mentioned terms to understand the workflow in a better way.

-  Data Subject :  A data subject is any person whose personal data is being collected, held or processed (https://eugdprcompliant.com/what-is-data-subject/)

- Consent : The informed, unambiguous and freely given permission from the data subject to have data relating to a Data Subject

- Refer this link for understanding key terms under GDPR (https://eugdprcompliant.com/key-terms/)

This workflow utilizes custom scripting feature offered from Treasure Data. Using the Python custom scripting, API calls are made to OneTrust and the data is ingested into Treasure Data.

## How does this data help?
 John Doe (Data Subject) visits a website (samplewebsite.com) which uses OneTrust for consent management. John Doe finds an interesting offer and clicks a link which takes him to a web form (collection point). This collectionpoint (webform) collects first name, last name, address, emailid and phone number and also request's  user consent  for Marketing Activation  and Marketing Analytics

 John Doe gives consent only to Marketing Analytics and  doesnt consent to Marketing Activation.

 To summarize, John Doe (Data Subject) visits a webform (collection Point) and gives consent to only Marketing Analytics (Purpose)

 A Marketing Analyst from samplewebsite.com wants to run an email campaign and target visitors with a new product offer.
 Without having consent information an analyst cannot
 -  Enrich the data and suppress the subjects who have not consented to a specific purpose (here, the pupose is Marketing Campaign)
 -  Cannot comply with privacy laws

Having access to OneTrust data on Treasure Data platform enables Marketing Department to enrich the data. In this example, John Doe's email id will be suppressed  for Marketing campaign. But, use his consent data for Marketing Analytics.

## Getting Started
These instructions will enable you to ingest the consent data from Onetrust.
Note: OneTrust currently hasnt made API documentation public. And API endpoints may change in future.

## Push the code and set variables
```
td wf push --project onetrust_integration
td wf secret --project onetrust_integration --set onetrustapikeys.yml #create a .yml file with all the secrets and set them for the project

```
|  Variable  | Description   | Example   |
| ------------ | ------------ | ------------ |
| `ot.apikey`  |  OneTrust API key that needs to be set as a secret and used for authentication with OneTrust  |  `003026bbc133714df1834b8638bb496e-8f4b3d9a-e931-478d-a994-28a725159ab9` |
| `ot.collectionendpoint`   | This endpoint configured as secret is used to get all the collection points configured in a website. Example : subscription webform where a data subject fills his/her PII data and consent to purposes is treated as one collection point | latest api end point details can be accesed through [OneTrust Developer Portal](https://developer.onetrust.com/consent-manager "OneTrust Developer Portal") .  Currently OneTrust hasnt made API documentation public.    |
| `ot.datasubjectpurpose`| This endpoint configured as secret is used to get all the datasubjects and the purpose to which they have consented . Example : John.Doe@abc.com is a datasubject who consented to purpose Marketing Analytics | latest api end point details can be accesed through [OneTrust Developer Portal](https://developer.onetrust.com/consent-manager "OneTrust Developer Portal") .  Currently OneTrust hasnt made API documentation public.  |
| `td.apikey` | An API key to be used in the script. Access Type must be `Master Key` | `1234/abcdefghijklmnopqrstuvwxyz1234567890` |
|`td.apiserver`| TD's API endpoint starting with `https:// ` | `https://api.treasuredata.com` |

Note: Refer [OneTrust Developer Portal ](https://developer.onetrust.com "OneTrust Developer Portal ") to identify the different endpoints.

## Process

![OneTrust](https://drive.google.com/uc?export=view&id=1nyvCECUJXS91ogmUpzbWTRpDezONrKjQ)

1. The script does API Authentication by passing the OneTrust key as a header when calling the endpoint and other paramters required for the endpoints as params.
2. After successful authentication API endpoints sends the payload as JSON
3. Parse the response and find the total number of pages
4. Call the API by passing page number (0..N) and store the data into a pandas dataframe
5. upload the dataframe to Treasure Data

Note: size is one of the param which defines total number of records per api call. 20 is default and 50 is maximum. In order to reduce number of API calls, use 50 for size param

## How Does Data Look Like ?

![Data Subject](https://drive.google.com/uc?export=view&id=14z1pVFtN-9JC95AW0uy8_b3i0-0jK_xF)


![Collection Point Details](https://drive.google.com/uc?export=view&id=157ONLAFTawZc8Fg3y97jVIzB3P-LAQ02)

