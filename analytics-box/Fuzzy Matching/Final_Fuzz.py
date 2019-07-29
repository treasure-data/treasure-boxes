#!/usr/bin/env python
# coding: utf-8

# In[1]:


#cfscores_output_uniques.csv - First Name and Last Name
#names - First Name


# In[770]:


import pandas as pd
import jellyfish as jf
import tdclient
import re
import fuzzywuzzy as fz
from fuzzywuzzy import fuzz
import time
import Levenshtein as ln
import string
import os
import glob
from ngram import NGram
import numpy as np
import Levenshtein 
from scipy import spatial


# In[771]:


#file1 = input("Enter your csv file path along with file name")
df = pd.read_csv('/Users/prachichavan/Downloads/cfscores_output_uniques.csv', header = 0 )
#df = pd.read_csv(file1)
df.shape


# In[772]:


#Function to combine different csv's for address in different files into one
def combine_address(mydir):
    os.chdir(mydir)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    return(combined_csv)
    


# In[773]:


#Cleaning the data 

#Remove punctuation , extra characters

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

#Remove numbers from a string

def remove_numbers(text):
     text = re.sub(r'\d+', '', text)
     return (text)
   
#Lower case all the strings

def lower_string(text):
     text = text.lower()
     return(text)
   



df['CLEAN_NAME'] = df['Last_First_Name'].apply(remove_punctuations)
df['CLEAN_NAME'] = df['CLEAN_NAME'].apply(remove_numbers)
df['CLEAN_NAME'] = df['CLEAN_NAME'].apply(lower_string)
df['NAME'] = df['CLEAN_NAME'] 



# In[774]:


#Soundex Algorithm 
def group_key(x):
   return jf.soundex(x)


df['GROUP_KEY'] = df['CLEAN_NAME'].apply(group_key)
df = df.sort_values(by = 'GROUP_KEY')


# In[775]:


#Master key
df['MASTER_KEY'] = 'Null'


# In[776]:


#Find the freqeuncy of the words in a single GROUP_KEY

df['FREQ'] = df.groupby('GROUP_KEY')['GROUP_KEY'].transform('count')
df1 = df[['GROUP_KEY','FREQ']]
df1 = df1.drop_duplicates()
df1['NAME'] = df.groupby('GROUP_KEY')['CLEAN_NAME'].first().to_frame().values

df1.reset_index(inplace=True)
df.reset_index(inplace=True)
df1_new = pd.DataFrame([df1.ix[idx] 
                       for idx in df1.index 
                        for _ in range(df1.ix[idx]['FREQ'])]).reset_index(drop=True)


#Concate two dataframes with the updated column
df['MASTER_KEY'] = df1_new['NAME']
  


# In[777]:


df.head(5)


# In[778]:


#Levenshtein distance measures for fuzzy matching

df['LEVENSTEIN_DIST_RATIO'] = 'Null'
for row,index in df.iterrows():
   df.loc[row,'LEVENSTEIN_DIST_RATIO'] = (Levenshtein.ratio(df.loc[row,'MASTER_KEY'],df.loc[row,'CLEAN_NAME'])) * 100
df = df.sort_values(['GROUP_KEY', 'LEVENSTEIN_DIST_RATIO'], ascending=[True, False])


# In[779]:


del df['FREQ']
df.head(5)


# In[780]:


#ngrams function

def ngram(df,text1,text2,leng, n=3):
    df[text1] = df[text1].str.replace(" ","")
    df[text2] ='Null'
    for index,row in df.iterrows():
        t = set([row[text1][i:i+n] for i in range(len(row[text1])-n+1)])
        df.loc[index,leng] = len(t)
        df.loc[index,text2] = [t]
    return df  

df = ngram(df,'CLEAN_NAME','CLEAN_NAME_NGRAM','LEN_CLEAN')
df = ngram(df,'MASTER_KEY','MASTER_KEY_NGRAM','LEN_MASTER')



for index,row in df.iterrows():
    df.loc[index,'Ngram'] = (len(df.loc[index,'CLEAN_NAME_NGRAM'].intersection(df.loc[index,'MASTER_KEY_NGRAM'])))

for index,row in df.iterrows():
    df.loc[index,'Ngram_Ratio'] = (((df.loc[index,'Ngram']) / (df.loc[index,'LEN_MASTER'])) * 100) 
    
#Dataframe cleaning    
del df['CLEAN_NAME_NGRAM']
del df['LEN_CLEAN']
del df['MASTER_KEY_NGRAM']
del df['LEN_MASTER']
del df['Ngram']


# In[781]:


#Cosine similarity

for index,row in df.iterrows():
        t = set([row['CLEAN_NAME'][i:i+3] for i in range(len(row['CLEAN_NAME'])-3+1)])
        u = set([row['MASTER_KEY'][i:i+3] for i in range(len(row['MASTER_KEY'])-3+1)])
        v = list(t.union(u))
        v1 = [(lambda x: 1 if x in row['CLEAN_NAME'] else 0)(x) for x in v]
        v2 = [(lambda x: 1 if x in row['MASTER_KEY'] else 0)(x) for x in v]
        df.loc[index,'Cosine'] = (spatial.distance.cosine(v1, v2))


# In[782]:


df.head(20)


# In[754]:


#Filter records based on the Levenshtein Distance
df[df['LEVENSTEIN_DIST_RATIO'] > 90]

