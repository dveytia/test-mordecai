## This version tries using tensorflow but still the number of threads are high



## Import modules
from mordecai import Geoparser
import pandas as pd
import pickle
import os
import sqlite3
import time
import tensorflow as tf
import concurrent.futures


################# 0. SET UP INPUTS #########################################
unseenTxt = '/home/dveytia/test-mordecai/data/raw-data/0_unique_references.txt' # change to unique_references2.txt?
relevanceTxt = '/home/dveytia/test-mordecai/data/raw-data/1_document_relevance_13062023.csv'
testLoc = False # Do I wante to test geoparsing works at beginning of script?
testSubset = True # Do I want to test this code on a subset of the data?
testSubsetRows = 100
num_threads = 5  # Replace this with the desired number of threads

tf.config.threading.set_intra_op_parallelism_threads(num_threads)
tf.config.threading.set_inter_op_parallelism_threads(num_threads)

################ 1. Test mordecai is working before proceeding ##################
## Set up mordecai geoparser
geo = Geoparser()

# test mordecai
if testLoc == True:
    print(geo.geoparse("I traveled from Oxford to Ottawa."))





###################### 2. Define functions for analysis #####################

## For Geoparsing text
def geoparse_text(text):
    return geo.geoparse(text)

## For flattening the list
def flat_result(result):
    df_geo = pd.DataFrame(result)
    df_geo = pd.concat([df_geo.drop(['geo'], axis=1), df_geo['geo'].apply(pd.Series)], axis=1)
    df_geo = df_geo[df_geo['lat'].notnull()] #Removing empty latitude rows
    df_geo.lat = df_geo.lat.astype(float) #Transforms to float
    df_geo.lon =df_geo.lon.astype(float) #Transforms to float
    df_geo = df_geo.drop_duplicates(['geonameid'],keep= 'last')
    df_geo = df_geo[['word', 'spans','country_predicted', 'country_conf', 'admin1', 'lat','lon', 'country_code3', 'geonameid', 'place_name', 'feature_class', 'feature_code']] 
    #df_geo = pd.concat([id, df_geo], axis=1)
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
df = df[['id', 'duplicate_id','text','title']]


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
t = time.time()



## Geoparse the text 
rows = [] # Initialize an empty list to store the rows

for i in list(range(len(df.index))):
    
    text = df["text"].iloc[i]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Submit the geoparsing task and get the future object
        future = executor.submit(geoparse_text,text)
        # Get the result when the task is completed
        result = future.result()
        
    if bool(result) == True: # if there is a result
        if 'geo' in result[0]: # also has to have a geo properties
            result_flat = flat_result(result)
            result_flat.insert(0, 'title', df['title'].iloc[i])
            result_flat.insert(0, 'duplicate_id', df['duplicate_id'].iloc[i])
            result_flat.insert(0, 'id', df['id'].iloc[i])
        
            rows.append(result_flat)

df_clean = pd.concat(rows) # bind all together


print(time.time() - t)  


## Check dataframe structure
print(df_clean.dtypes)
print(df_clean[0:5])
df_clean.head(5)


################ 5. Write output file ###################

## Save as a .csv
df_clean.to_csv('/home/dveytia/test-mordecai/outputs/geoparsed-records.csv', index=False)