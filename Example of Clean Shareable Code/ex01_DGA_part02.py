# -*- coding: cp1252 -*-
import pandas as pd
import numpy as np
import re
import scipy
import sklearn
from sklearn import linear_model
import xgboost as xgb
import matplotlib
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score


train_data=pd.read_csv('input/dga-dataset_train.csv',index_col =0)
test_data=pd.read_csv('input/dga-dataset_test.csv',index_col =0)


#May want to try using svd for transformation down the road when coming back to improve




# n-grams (counting the number of times a particular string of length 'n' occures) were not used due to memory and processing requirements and the model can be useful without it.
#Jibberish removal indicators. Most words do not have alot of consonants in sequence with a different consonant. Thus counting sequential consonants and vowels is a good indicator for missplellings and jibbers.
def vowel_count(site):
	return len(re.findall(r'[aeiouy]',site))+0.0

def consonant_sequence(site):
	#These functions replace any pair of repeating consonants with the repeated consonant (i.e. 'rr'->'r' or 'tt'->'t') and the count pairs of sequential consonnts (ex. 'rt'=1 or 'prt'=2)
	return len(re.findall(r'[qwrtpsdfghjklmnbvcxz][qwrtpsdfghjklmnbvcxz]',re.sub(r'(.)\1{1,}',r'\1',site)))+0.0

train_data['vowel_count']=train_data['site'].apply(lambda site: vowel_count(site))
train_data['consonant_sequence']=train_data['site'].apply(lambda site: consonant_sequence(site))

test_data['vowel_count']=test_data['site'].apply(lambda site: vowel_count(site))
test_data['consonant_sequence']=test_data['site'].apply(lambda site: consonant_sequence(site))

# Randomaly generated primary domains with a lot of characters would be expected to have more diverse characters since its randomly choosing letters and may not even pay attention to linguistic nuances such as vowels, syllibuls, etc. Also even at the word level we would expect certain words (and thus their letters) to occur more often together thus having a reducd entropy
def letter_entropy(site):
	key_letters={intersected_letter:0 for intersected_letter in list(set(list(site)).intersection(set([letter for letter in 'qwertyuioplkjhgfdsazxcvbnm'])))}
	total_characters=len(re.findall('[a-z]',site))+0.0
	for letter in key_letters.keys():
		key_letters[letter]=site.count(letter)/total_characters
		key_letters[letter]=np.log(key_letters[letter])*key_letters[letter]
	#The entropy formula has a physics constant but the physics constant isn't used as this isn't physics and any constant may be captured in regression models and in decision trees the constant will not be as useful
	return sum(key_letters.values())


train_data['letter_diversity']=train_data['site'].apply(lambda site: letter_entropy(site))	

#Counting characters, symbols, numbers and letters just as a precaution
train_data['character_count']=train_data['site'].apply(lambda site: len(site)+0.0)

test_data['letter_diversity']=test_data['site'].apply(lambda site: letter_entropy(site))								
test_data['character_count']=test_data['site'].apply(lambda site: len(site)+0.0)




def num_count(site):
	return sum([1.0 if character in ['1','2','3','4','5','6','7','8','9','0'] else 0.0 for character in site])

def letter_count(site):
	return sum([site.count(letter) for letter in 'qwertyuioplkjhgfdsazxcvbnm'])+0.0

train_data['number_count']=train_data['site'].apply(lambda site: num_count(site))
train_data['letter_count']=train_data['site'].apply(lambda site: letter_count(site))
train_data['consonant_count']=train_data['letter_count']-train_data['vowel_count']
train_data['symbol_count']=train_data['character_count']-train_data['letter_count']-train_data['number_count']



test_data['number_count']=test_data['site'].apply(lambda site: num_count(site))
test_data['letter_count']=test_data['site'].apply(lambda site: letter_count(site))
test_data['consonant_count']=test_data['letter_count']-test_data['vowel_count']
test_data['symbol_count']=test_data['character_count']-test_data['letter_count']-test_data['number_count']








# Deleting columns that won't be used such as site (since using random strings for models without replacing them with features is a complex and very time consuming task) and source

del train_data['site']
del train_data['source']


del test_data['site']
del test_data['source']

x_cols=list(set(train_data.columns)-set(['type']))
print(x_cols)

### Checking for dgas length as if there lengths happen to be skewed this could result in a blind spot of the program. However since one or two word website names are more likely to be bought already (I assume) that makes it cost-prohibitative for hackers to use many sights on the lower end of the length scale.
print('string length')
print('max length: '+str(max(train_data['character_count'])))
print('min length: '+str(min(train_data['character_count'])))
print('\n')



#Showing range of variables as to get a better idea of scale in regards to their coeficients in logistic regression model
for x_variable in x_cols:
	print('%s range is: %s to %s' % (x_variable,min(train_data[x_variable]),max(train_data[x_variable])))
	
print('\n\n\n')

#Create object to store model by accuracy and return model with highest accuracy
models={}

#Checking the Y value is evenly balanced, this also tells us the null accuracy rate (how accurate we'd be if we just labeled every record by the most probable label), So that is the baseline we must beat
print('Percent of training data with DGAs: {} \nPercent of test data with DGAs: {}'.format(sum(train_data['type'])/(train_data.shape[0]+0.0),sum(test_data['type'])/(test_data.shape[0]+0.0)))


# Storing all models for comparision and visualization
all_models={}

# Determined features did not need to be normalized now since normalizing data befor modeling it will effect the correlations of the features

print('\n\n')




#### Training models and displaying confusion matrix (predictions is columns and true values are rows) and accuracy; cross validation was not used for simpli

## The coeficients and feature importance variable shows how useful the transformations I decided on are to the model
# Primarily stuck to default parameters for quick turn around time

print('logistic')
from sklearn.linear_model import LogisticRegression
logistic = LogisticRegression(class_weight = 'balanced',solver='newton-cg')

logistic.fit(train_data[x_cols].copy(),train_data['type'].copy())
y=logistic.predict(test_data[x_cols])
print('Accuracy of {}'.format(accuracy_score(test_data['type'].tolist(), y)))
print('\n')
cm=confusion_matrix(test_data['type'],y)
print('Confusion Matrix:\n {}'.format(cm))
print('\n')
print('Precision: {} and Recall: {}'.format(  (cm[1][1]/(cm[1][1]+cm[0][1])+0.0),(cm[1][1]/sum(cm[1])+0.0)  ))
print('\n')
print('feature Coefficients:')
for variable_coef in zip(x_cols,logistic.coef_[0]):
	print(variable_coef[0]+': '+str(variable_coef[1]))
print('\n')
print('Y take values of: {}'.format(set(y)))
print('\n\n\n')

models[accuracy_score(test_data['type'].tolist(), y)]=logistic
all_models['logistic']=logistic





import xgboost as xgb

bst = xgb.XGBClassifier(max_depth=15,
                           min_child_weight=1,
						   n_jobs=1,
                           learning_rate=0.1,
                           silent=True,
                            eval_metric='auc',
                           objective='binary:logistic',
                           max_delta_step=2,
                           subsample=1,
                           colsample_bytree=1,
                           colsample_bylevel=1,
                           reg_alpha=0,
                           reg_lambda=0,
                           scale_pos_weight=1,
                           seed=1,
                           missing=None)

bst.fit(train_data[x_cols].copy(),train_data['type'].copy())

y=bst.predict(test_data[x_cols])

print('grid xgb')
print('\n')
print('Accuracy of {}'.format(accuracy_score(test_data['type'].tolist(), y)))
print('\n')
cm=confusion_matrix(test_data['type'],y)
print('Confusion Matrix:\n {}'.format(cm))
print('\n')
print('Precision: {} and Recall: {}'.format(  (cm[1][1]/(cm[1][1]+cm[0][1])+0.0),(cm[1][1]/sum(cm[1])+0.0)  ))
print('\n')
print('feature importance:')
for variable_importance in zip(x_cols,bst.feature_importances_):
	print(variable_importance[0]+': '+str(variable_importance[1]))
models[accuracy_score(test_data['type'].tolist(), y)]=bst
all_models['xgboost']=bst
print('\n')
print('Y take values of: {}'.format(set(y)))
print('\n\n\n')







from sklearn import svm


print('linear')
lin_svc = svm.SVC(kernel='linear', C=1.0, probability=True).fit(train_data[x_cols].copy(),train_data['type'].copy())
y=lin_svc.predict(test_data[x_cols])
print('\n')
print('Accuracy of {}'.format(accuracy_score(test_data['type'].tolist(), y)))
print('\n')
cm=confusion_matrix(test_data['type'],y)
print('Confusion Matrix:\n {}'.format(cm))
print('\n')
print('Precision: {} and Recall: {}'.format(  (cm[1][1]/(cm[1][1]+cm[0][1])+0.0),(cm[1][1]/sum(cm[1])+0.0)  ))
print('\n')
print('feature Coefficients:')
for variable_coef in zip(x_cols,lin_svc.coef_[0]):
	print(variable_coef[0]+': '+str(variable_coef[1]))
print('\n')
print('Number of support vectors: {}'.format(len(lin_svc.support_)))
print('\n')
print('Y take values of: {}'.format(set(y)))
print('\n\n\n')

models[accuracy_score(test_data['type'].tolist(), y)]=lin_svc
all_models['lin_svm']=lin_svc
train_small=train_data.sample(n=100)

print('poly')
poly_svc = svm.SVC(kernel='poly', degree=8, C=1.0, probability=True).fit(train_small[x_cols],train_small['type'])
y=poly_svc.predict(test_data[x_cols])
print('\n')
print('Accuracy of {}'.format(accuracy_score(test_data['type'].tolist(), y)))
print('\n')
cm=confusion_matrix(test_data['type'],y)
print('Confusion Matrix:\n {}'.format(cm))
print('\n')
print('Precision: {} and Recall: {}'.format(  (cm[1][1]/(cm[1][1]+cm[0][1])+0.0),(cm[1][1]/sum(cm[1])+0.0)  ))
print('\n')
print('Number of support vectors: {}'.format(len(poly_svc.support_)))
print('\n')
print('Y take values of: {}'.format(set(y)))
print('\n\n\n')

models[accuracy_score(test_data['type'].tolist(), y)]=poly_svc
all_models['poly_svm']=poly_svc

print('rbf')
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=1.0, probability=True).fit(train_small[x_cols],train_small['type'])
y=rbf_svc.predict(test_data[x_cols])
print('\n')
print('Accuracy of {}'.format(accuracy_score(test_data['type'].tolist(), y)))
print('\n')
cm=confusion_matrix(test_data['type'],y)
print('Confusion Matrix:\n {}'.format(cm))
print('\n')
print('Precision: {} and Recall: {}'.format(  (cm[1][1]/(cm[1][1]+cm[0][1])+0.0),(cm[1][1]/sum(cm[1])+0.0)  ))
print('\n')
print('Number of support vectors: {}'.format(len(rbf_svc.support_)))
print('\n')
print('Y take values of: {}'.format(set(y)))
print('\n\n\n')


models[accuracy_score(test_data['type'].tolist(), y)]=rbf_svc
all_models['rbf_svm']=rbf_svc


##since all models have returned a binary value and their accuracy, and to quickly showcase the progress of the project there is no need to take the probabilities to then do AUC and ROC analysis for this stage in the project.

outFile= open('output/model.txt', 'wb')
pickle.dump({'model':models[max(models.keys())],'init':1,'columns':x_cols},outFile)
outFile.close()

outFile= open('output/models.txt', 'wb')
pickle.dump(all_models,outFile)
outFile.close()
