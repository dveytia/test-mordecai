

## Import modules
from mordecai import Geoparser
import pandas as pd
import pickle
import os
import sqlite3
from multiprocessing.pool import ThreadPool as Pool


################# 0. SET UP INPUTS #########################################
unseenTxt = '/home/dveytia/test-mordecai/data/raw-data/0_unique_references.txt' # change to unique_references2.txt?
relevanceTxt = '/home/dveytia/test-mordecai/data/raw-data/1_document_relevance_13062023.csv'
n_threads = 10 # number of threads to parallelize on
testSubset = True
testSubsetRows = 100

################ 1. Test mordecai is working before proceeding ##################
## Set up mordecai geoparser
geo = Geoparser()

# test mordecai
testLoc = geo.geoparse("I traveled from Oxford to Ottawa.")
print(testLoc)



###################### 2. Define functions for analysis #####################

## For Geoparsing text
def geoparse_text(text):
    return geo.geoparse(text)

## format geoparsed dataframe
def flat_df(df):
    df_geo = df[df["geoparse"].str.len() != 0] #subset where geoparse string is not empty
    df_geo = df_geo.explode('geoparse') #Transforms each element of a list to a row and replicates index and all other columns. When more than one place name appears it creates more than one row.
    df_geo = pd.concat([df_geo.drop(['geoparse'], axis=1), df_geo['geoparse'].apply(pd.Series)], axis=1) #Extract from dic
    df_geo = pd.concat([df_geo.drop(['geo'], axis=1), df_geo['geo'].apply(pd.Series)], axis=1)
    df_geo = df_geo[df_geo['lat'].notnull()] #Removing empty latitude rows
    df_geo.lat = df_geo.lat.astype(float) #Transforms to float
    df_geo.lon =df_geo.lon.astype(float) #Transforms to float
    return df_geo


############### 3. Read in data and format ####################

# Load unseen documents 
unseen_df = pd.read_csv(unseenTxt, delimiter='\t')
unseen_df = unseen_df.rename(columns={'analysis_id':'id'})
unseen_df=unseen_df.dropna(subset=['abstract']).reset_index(drop=True) # drop NA abstracts

# Load predictions of relevance (screen decisions)
pred_df = pd.read_csv(relevanceTxt)

# merge relevance predictions into unseen df
df = unseen_df.merge(pred_df, how="left")
df['seen']=0

# Choose which predictiction boundaries to apply
df = df[df['0 - relevance - upper_pred']>=0.5]

# combine title and abstract text into one variable
df['text'] = df['title'].astype("str") + ". " + df['abstract'].astype("str") + " " + "Keywords: " + df["keywords"].astype("str")
df['text'] = df.apply(lambda row: (row['title'] + ". " + row['abstract']) if pd.isna(row['text']) else row['text'], axis=1)

# subset to only the columns I need for analysis
df = df[['id', 'duplicate_id','text']]


# replace "the United States" with "United States" to avoid returning the virgin islands
# the (?i) means it is case insensitive
df['text'] = df.text.replace("(?i)the (?i)United (?i)States", "United States", regex=True) 

print(df.shape) 
print(df.head(3))
print("should be 61656 rows")

if testSubset == True:
    df = df.head(testSubsetRows)
    print('test subset size')
    print(df.shape)



###################### 4. Analysis ##############################

## Geoparse the text 
if __name__ == '__main__':
    with Pool(n_threads) as pool:
        df["geoparse"]=pool.map(geoparse_text,df["text"].astype('str'))


## Format the dataframe    
df_clean = flat_df(df)
df_clean = df_clean.drop_duplicates(['id','geonameid'],keep= 'last')

## Check dataframe structure
print(df_clean.dtypes)
print(df_clean[0:5])
df_clean.head(5)


################ 5. Write output file ###################

## Save as a .csv
df_clean.to_csv('/home/dveytia/test-mordecai/outputs/geoparsed-records.csv', index=False)