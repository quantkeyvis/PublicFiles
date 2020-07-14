# -*- coding: cp1252 -*-
import os
import re
import sys
import pandas
import random
import numpy as np
import sklearn.utils


### The tld related imports were meant to be used to extract primary-domain
# but is commented out because it returned too many urls as not urls, however it was based on a compiled list of domains and is not removed in the script in case it can be repurposed in the future for benchmarking, supplimenting etc

'''
#Get most up-to-date list for domain level extraction
from tld.utils import update_tld_names
from tld import get_tld
update_tld_names()
full_data['site']=full_data['site'].apply(lambda x: get_tld(x, as_object=True).domain )
'''


#Load the data into a dataframe splitting into columns and naming the columns
full_data=pandas.read_csv('input/dga-dataset_clean.txt',names=['site','source','type'])
print(full_data)

#Standardize the text to be all lowercase and convert any missing data to a string (which is the data type of all the non-missing data)
for name in ['site','source','type']:
	full_data[name]=full_data[name].apply(lambda x: x.lower() if type(x)!=type(float()) else ' ')
	
#Correct misspellings, based on this sample simply determining legit or not legit by the first letter is good enough (so no need for word matching by determining type of misspelling)
full_data['type']=full_data['type'].apply(lambda x: 'dga' if x[0]=='d' else ('legit' if x[0]=='l' else x))


#printing the basic set of the two columns to make sure changes until now ave created the proper elements (basically make sure nothing unexpected shows up in the data)
print(set(full_data['type']))
print('\n\n')
print(set(full_data['source']))
print('\n\n')



# Store sites with no label for testing later
missing_data=full_data[full_data['type']==' '].copy()
print('Number of missing types: {}'.format(missing_data.shape[0]))
missing_data.to_csv('output/dga_dataset_missing.csv')
missing_data=None




#Remove unlabeled sites

full_data=full_data[full_data['type']!=' ']
full_data['type']=full_data['type'].apply(lambda x: 1.0 if x[0]=='d' else 0.0)



#### Extract Primary Domian


def domain_extract(site):
	#Remove unneeded url segments that are likely top-level domains
	site_segments={len(site_segment):site_segment for site_segment in re.sub(r'(^www[.]|^www1[.]|^https://|^http://|^[a-z][.]|[.][a-z]{1,3}$)','',site).split('.')}
	#Taking the longest segment since it may consume too much time to find or create a more dynamic domain extractor to ensure we aren't getting sub-domains
	return site_segments[max(site_segments.keys())]


full_data['site']=full_data['site'].apply(lambda site: domain_extract(site))



#Split Data for training and validation
n_rows=full_data.shape[0]
split=int(round(0.75*n_rows))
full_data=full_data.copy()

# Shuffling the data before split in case there is some unknown sequential effect (maybe more DGA sites were collected at first)
full_data = sklearn.utils.shuffle(full_data)
train_data=full_data[:split]
test_data=full_data[split:]
train_data.to_csv('output/dga-dataset_train.csv')
test_data.to_csv('output/dga-dataset_test.csv')
