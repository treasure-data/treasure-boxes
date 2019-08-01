
# Fuzzy Matching to identify similar profiles in treasure data  
  
This project provides the workflows necessary to use Fuzzy Matching algorithms like Levenshtein to do probabilistic matching of the profiles. Once higher probability of similar profiles is gathered, they can further be compared with behavioral data using deterministic matching. Report is generated to give an overview of similar profiles and relevant profiles then can be chosen to stay into treasure data platform. For more description , please refer to the Treasure Box overview page for [Fuzzy Matching](https://boxes.treasuredata.com/hc/en-us/articles/360032618714-Fuzzy-Matching-on-PII-data)  
  
## Getting Started  

1.Download this folder locally.
2.Use [TD Toolbelt](https://support.treasuredata.com/hc/en-us/articles/360001262207-Treasure-Workflow-Quick-Start-using-TD-Toolbelt-in-a-CLI) to upload this folder as a Treasure Workflow project into your Treasure data account  
  
### How it works

Here is a brief description what each task in the workflow do

1.First Name and Last Name table and column information is provided
2.Data Cleaning task removes the punctuations, numbers and extra characters from the column
3.Soundex Algorithm is implemented which generates a four-character code based upon the pronunciation of the English words
4.Master key is generated for each group to make implementation of Fuzzy Matching algorithms easier
5.Fuzzy Matching algorithms like Levenshtein ratio are used to find probability of profiles being similar
6.Cut – off can be decided based on the Levenshtein ratio calculated to get the similar profiles.
7.Create a Match store which holds the information of group_key and index of corresponding similar profiles as a metadata for easy retrieval of profiles
8.Similar profiles gathered based on the cut off value can be visualized using any reporting tool.

### Outputs  
  
Here are snapshots how this workflow results in TD.

### Before Data Cleaning

![Image description]
 (https://ibb.co/rp1njbn))

### After Data Cleaning

<![if !vml]>![](file:////Users/prachichavan/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image002.png)<![endif]>

### Soundex Algorithm

<![if !vml]>![](file:////Users/prachichavan/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image003.png)<![endif]>

### Master Key Creation

<![if !vml]>![](file:////Users/prachichavan/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.png)<![endif]>

### Levenshtein Algorithm

<![if !vml]>![](file:////Users/prachichavan/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image005.png)<![endif]>

### Match store

<![if !vml]>![](file:////Users/prachichavan/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.png)<![endif]>

### Sample Dashboard using Treasure Data Reporting

![alt tag](https://i.postimg.cc/mDjpC8zH/Screen-Shot-2019-07-29-at-4-54-33-PM.png)

### Questions

Please feel free to reach out to [support@treasure-data.com](mailto:support@treasure-data.com) with any questions you have about using this code for Fuzzy Matching
