# Data Profiling & PII Detection in Treasure Data 


## Introduction 

The aim of this workflow is to provide a high-level design pattern to profile data in Treasure Data and also identify columns with PII.This workflow can be modified further based on the needs of the project. Data Profiling is the process of examining the data available and collecting statistics or informative summaries about that data.Data profiling tasks can be done on single column or multiple columns. This workflow is focused on single column analysis for integer, double and varchar data types. 

  * Single Column Analysis  
     * Integer and Double data type
         * Number of Distinct values 
         * Min and Max value 
         * Number of NULL values
         * Average value 
         * Top N Min and Max values 
         * Value Frequency 

     * Varchar data type 
        * Number of NULL values
        * Number of Distinct values
        * Top N Min and Max lenght of string  
        * Value Frequency 
        * PII detection for common PII elements such as IPv4,IPv6, SSN , US-Phone# 
      

## Uses of Data Profiling

    * Data Analytics 
      * Profiling as preparation and for initial insights

    * Data cleansing
       * Patterns and violations

    * Query optimization
       * Cardinality estimations for joins

    * Data management
       * Find unique constraints 

## Uses of PII detection 
  * Limit PII exposure to safegaurd customer data
  * Being complaint with data security best practices

## Getting Started  
 Data Profiling workflow consists of three components
  * config file
  * sql files
  * wf script (.dig file)



### How to run workflow

Step 1: create a database dataprofiling_results where all the profiling results will be stored.

Step 2:  modify the Config file to set the following parameters   

```yml
   source_database : 'Database where source table (source which needs to be profiled)'
   source_table : 'tableon which data profiling process is run' 
   min_max_limit : 5  #Top N values for min and max 
   val_freq_limit : 5  #Parameter to set number of TOP N freq values  
   data_threshold : 0.8  # parameter  
   sample_size : 25  # percentage of data which taken as a sample for PII detection 
   ```            
  

 Output: The process creates the following tables in dataprofile_results database.This database needs to be created in Treasure Data before running the profiling workflow. 

 | Output Table                       | Description                                                                                                                           |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| ${source_table}_column_metadata    | uses INFORMATION_SCHEMA.columns source to create a table with column details                                                          |
| ${source_table}_profile_bigint     | basic numeric statistics profile results are outputted to this table for columns of integer type                                      |
| ${source_table}_profile_bigint_vf  | Top N (defined in config value as val_freq_limit) value frequency results for each of the integer type                                |
| ${source_table}_profile_double     | basic numeric statistics profile results are outputted to this table for columns of double type                                       |
| ${source_table}_profile_double_vf  | Top N (defined in config value as val_freq_limit) value frequency results for each of the double type                                 |
| ${source_table}_profile_varchar    | basic statistics profile for datatype varchar like min length of string, max length ,number of null values, number of unique values   |
| ${source_table}_profile_varchar_vf | Top N (defined in config value as val_freq_limit) value frequency results for each of the type varchar                                |
| ${source_table}_profile_pii        | This table has all the columns listed along with a boolean value (Yes/No) testing various if it fits various PII pattern              |


### PII detection Process

 This process samples the data using `TABLESAMPLE BERNOULLI()` method which takes an input of percentage of data needed for sampling.The higher the percentage the more accurate the results are. but,the tradeoff is query run time.
 The script shown below flags a column if it fits the pattern of following PII elements  

| PII                                    | REGEX                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SSN                                    | ^\d{3}-\d{2}-\d{4}$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| IP address                             | ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| IPV6 address                           | (([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])) |
| Email address                          | \b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Phone Number (US only xxx-xxx-xxxx)    | ^(?:\(?([0-9]{3})\)?[-.●]?)?([0-9]{3})[-.●]?([0-9]{4})$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Phone Number (US only +1 xxx-xxx-xxxx) | ^(?:\+?1[-.●]?)?\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |


### PII SQL

 ```  SQL
SELECT 
 '${source_database}.$(source_table}' as  schema 
,'${column}' as  column 
,case 
 when cast(count_if(REGEXP_LIKE(${column},'^\d{3}-\d{2}-\d{4}$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ssn  
,case 
 when cast(count_if(REGEXP_LIKE(${column},'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ipaddress 
,case 
 when cast(count_if(REGEXP_LIKE(${column}, '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_ipv6_address 
 ,case 
 when cast(count_if(REGEXP_LIKE(${column}, '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 else 'No' end as is_email
 ,case 
 when cast(count_if(REGEXP_LIKE(${column}, '^(?:\(?([0-9]{3})\)?[-.●]?)?([0-9]{3})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 when cast(count_if(REGEXP_LIKE(${column}, '^(?:\+?1[-.●]?)?\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)>${data_threshold} then 'Yes' 
 when cast(count_if(REGEXP_LIKE(${column}, '^\(?([2-9][0-8][0-9])\)?[-.●]?([2-9][0-9]{2})[-.●]?([0-9]{4})$')=TRUE) as double)/count(*)> ${data_threshold} then 'Yes' 
else 'No' end as is_phone_usa
FROM ${source_database}.$(source_table} TABLESAMPLE BERNOULLI(${sample_size})

 ```


