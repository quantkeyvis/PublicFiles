# -*- coding: cp1252 -*-
#python -m pip install blahblah
import BeautifulSoup as bs
import numpy as np
import pandas as pd
import textmining as tm
#import Dcluster as dcl
import urllib
import sys
import re
import random
import numpy as np
import textmining as tm
import sys
import re
import random
import glob
import pickle
from nltk.corpus import stopwords




stop_words = stopwords.words("english")

stop_codec=[u'\xd2',u'\xe0',u'\u2011',u'\ude31',u'\ude0d',u'\ud83d',u'\u05d3',u'\u05de',u'\u05d7',u'\u202c',u'\xe4',u'\xf6',u'\u2013',u'\xf3',u'\xeb',u'\xad',u'\xf4'
            ,u'\u2014',u'\u0302',u'\u200b',u'\xa9',u'\xc9',u'\xed',u'\xfc',u'\xc1',u'\xd6',u'\U0001f9c0',u'\u2013',u'\xe8',u'\u20ac',u'\u2022',u'\u2026',u'\xe1'
            ,u'\xf1',u'\xfa',u'\xe7',u'\xa3',u'\xef','\xa0',u'\u2019',u'\xe9',u'\u201c',u'\u201d',u'0xc3',u'\u2018',u'\u0131',u'\u011f',u'\u015f',u'\u0159',u'\u0101'
            ,u'\u0161',u'\u0301',u'\xbf',u'\xe1',u'\ufffd',u'\u20b9']

pickle_loc=open(r'articleslinkstitle2017-10-19.pickle',"rb")
sites=pickle.load(pickle_loc)
pickle_loc.close()
[u'articles', u'Titles', u'site', u'Links', u'Time_Stamp']
docs={}
#stop_words.extend([])
print('got it')
for i in xrange(len(sites['articles'])/8):
    #text_file = open(r'doc'+str(i)+'.txt', "w")
    #text_file.write(fil)
    if len(sites['articles'][i])<1284:
        continue
    sites['Links'][i]=sites['Links'][i]+str(i)
    docs[sites['Links'][i]]=sites['articles'][i]
    #text_file.close()
print('This many docs were looked at: '+str(i)+' \n and this many were real: '+str(len(docs.keys())))

print('\n')
sites=docs.keys()
for i,index in enumerate(sites):
    doc=re.sub('[^\w]',' ',docs[index].lower())
    doc=re.sub("\n", " ",doc)
    doc=re.sub("[123456789]", "#",doc)
    doc=re.sub("###", "#",doc)
    doc=re.sub("##", "#",doc)
    doc=re.sub("\t", " ",doc)
    for j in stop_words:
        doc=re.sub('( |$|^)'+j+'( |$|^)', " ",doc)
    for j in stop_codec:
        doc=re.sub('( |$|^)'+j+'( |$|^)', "",doc)
    doc=re.sub('( |$|^)t( |$|^)', "t",doc)
    doc.replace("  "," ")
    docs[index]=doc
    doc_split=doc.split(" ")
    if i==0:
        doc_set=list(set(doc_split))
    else:
        doc_set.extend(list(set(doc_split)))
doc_set=list(set(doc_set))
word_cnt={}
for i in doc_set:
    word_cnt[i]=0
    for j in sites:
        word_cnt[i]+=docs[j].count(i)
cut_off=np.percentile(np.array(word_cnt.values()),20)
print('Word Cut-off is: '+str(cut_off))
cut_off=len(sites)
for i in doc_set:
    if word_cnt[i]<=cut_off:
        for j in sites:
            docs[j]=re.sub('( |$|^)'+i+'( |$|^)',' ',docs[j])
        del word_cnt[i]
doc_set=word_cnt.keys()
##rmv_wd=[]
##for i in doc_set:
##    if '\\' in i:
##        print(i)
##        rmv_wd.append(i)
##print('\n')
##decide=input("Remove this list of 'words'? (y/n)")
##if decide=='y':
##    doc_set=list(set(doc_set)-set(rmv_wd))
word_cnt=None
print('doc splitted')
docs_names= sites
doc_dict=dict.fromkeys(doc_set,0)
tdl={}
sites=None
print('index made')
print(len(docs_names))
while docs!={}:
    doc_dict_temp=dict(doc_dict)
    index=docs_names[0]
    del docs_names[0]
    doc_split=docs[index].split(" ")
    del docs[index]
    for word in doc_split:
        try:
            doc_dict_temp[word]+=1
        except KeyError:
            #print('missed words somehow')
            #sys.exit()
            pass
    tdl[index]=doc_dict_temp
print('have tdm')
data=pd.DataFrame(tdl)
tdl=None
data.to_csv(r'play_tdm.csv')
sys.exit()
6421
