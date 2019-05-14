import sklearn
import argparse
import scipy
import pickle
import re
import numpy as np
import pandas as pd

inFile=open('input/model.txt','rb')
model=pickle.load(inFile)
inFile.close()

# The transforming functions were copied from the Model_Selection file since they don't require special packages it was simplier to just copy them in the script rather than create another script to upload

def domain_extract(site):
	site_segments={len(site_segment):site_segment for site_segment in re.sub(r'(^www[.]|^www1[.]|^https://|^http://|^[a-z][.]|[.][a-z]{1,3}$)','',site).split('.')}
	return site_segments[max(site_segments.keys())]




#Creating jibberish removal indicator. Most words dont have alot of consonants in sequence with a different consonant. Thus counting sequential consonants is a good indicator for missplellings and jibbersish that might have been created from random generators.

def vowel_count(site):
	return len(re.findall(r'[aeiouy]',site))+0.0
def consonant_sequence(site):
	return len(re.findall(r'[qwrtpsdfghjklmnbvcxz][qwrtpsdfghjklmnbvcxz]',re.sub(r'(.)\1{1,}',r'\1',site)))+0.0



# Randomaly generated domains with a lot of characters would be expected to have more diverse characters since its randomly choosing letters and may not even pay attention to linguistic nuances such as vowels, syllibuls, etc
def letter_entropy(site):
	key_letters={intersected_letter:0 for intersected_letter in list(set(list(site)).intersection(set([letter for letter in 'qwertyuioplkjhgfdsazxcvbnm'])))}
	total_characters=len(re.findall('[a-z]',site))+0.0
	for letter in key_letters.keys():
		key_letters[letter]=site.count(letter)/total_characters
		key_letters[letter]=np.log(key_letters[letter])*key_letters[letter]
	return sum(key_letters.values())


def number_count(site):
	return sum([1.0 if character in ['1','2','3','4','5','6','7','8','9','0'] else 0.0 for character in site])

def letter_count(site):
	return sum([site.count(letter) for letter in 'qwertyuioplkjhgfdsazxcvbnm'])+0.0



def classify(site):
	#Extracting the features needed for classification
	primary_domain=domain_extract(site)
	rec={}
	rec['consonant_sequence']=consonant_sequence(primary_domain)
	rec['letter_count']= letter_count(primary_domain)
	rec['vowel_count']=vowel_count(primary_domain)
	rec['letter_diversity']=letter_entropy(primary_domain)						
	rec['character_count']=len(primary_domain)+0.0
	rec['number_count']= number_count(primary_domain)
	rec['consonant_count']= rec['letter_count']-rec['vowel_count']
	rec['symbol_count']= rec['character_count']-rec['letter_count']-rec['number_count']
	#Formatting the data to be accepted by the model and then getting the classification
	site_legitimacy=model['model'].predict(pd.DataFrame(rec,index=[0])[model['columns']])[0]
	if site_legitimacy>= 0.5:
		return 'DGA'
	else:
		return 'Legit'

	
### Printing out a test case remove hashtags of the following two lines to automatically run a test casee when script is called.
print('Site: www.567u6hy46uuuuhhhhh.org')
print(classify('www.567u6hy46uuuuhhhhh.org'))


### This section of the code is included incase you want to also use the model in command line. 
### Simply navigate to the folder containing this file (or create an environment variable so you don't have to navigate) type 'python3' (or python if you only have python 3 installed) 'DGA_Class <site>' replace <site> with the url you want to be classified.
if __name__ =='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('site', help="Website")
	args=parser.parse_args()
	classify(args.site)
