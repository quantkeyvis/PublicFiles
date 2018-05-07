import requests
import BeautifulSoup
import nltk
import re
import sys
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import pickle
import datetime
#import urllib.request
#from selenium import webdriver
import lxml


print 'starting'
link_types=['.wav','.wma','.m4a','.mpeg','.jpeg','.mpg','.mpa','.asf','.avi','.gif','.wmv','.aif','.mpa','mailto:','.mov','.mp3','.mp4' ,'instagram.com','twitter.com' ,'facebook.com' ,'.php','javascript:']
ref_notes=['#','#content','#main-content','stream.php']
sys.setrecursionlimit(100000)
pickle_loc=open("sites.pickle","rb")
sites=pickle.load(pickle_loc)
pickle_loc.close()
stamp=str(datetime.datetime.now()).split(" ")[0]
if os.path.isfile(r'articleslinkstitle'+stamp+'.pickle'):
    sys.exit()
test="https://www.theguardian.com/uk"
#print soup.prettify()
print 'start'
none_http_links=[]
art_links=[]
summary=[]
name_news=[]
arts=[]
errs=[]
country=[]
for i,state in enumerate(sites.keys()):
    for site in sites[state]:
        news_name=site.replace("https://www.", "")
        news_name=news_name.replace("http://www.", "")
        news_name=news_name.replace("https://", "")
        news_name=news_name.replace("http://", "")
        news_name=news_name.replace(".org", " ")
        news_name=news_name.replace(".com", " ")
        news_name=news_name.replace(".tv", " ")
        news_name=news_name.replace(".net", " ")
        news_name=news_name.replace(".co.", " ")
        news_name=news_name.replace(".", " ")
        news_name=news_name.split(' ')[0]
        if (r'http://' not in site and r'https://' not in site):
            site=r'http://'+site
        try:
            r = requests.get(site,timeout=10.0)
            print(news_name)
        except Exception as e:
            try:
                r = requests.get(site,timeout=10.0)
                print(news_name)
            except Exception as e:
                print(news_name+':  '+str(type(e)))
                print(site)
                print('\n')
                errs.append(str(type(e)))
                continue
        #driver = webdriver.PhantomJS(executable_path='PATH TO phantomjs')
        #driver.get(url)
        #r = driver.page_source
        soup = bs(r.content,"lxml")
        #soup = bs(r,"lxml")
        #### fix for dif webs
        for link in soup.find_all("a"):
            ref=link.get("href")
            if ref==None or sum([i in ref for i in link_types])>=1 or ref=='' or ref[0]=='#' or ref in ref_notes:# or link.get("data-link-name")!="article":
                continue
            else:
                if ref[0]=='/':
                    ref=site+ref
                elif ('http:' not in ref and 'www.' not in ref and 'https:' not in ref):
                    ref=site+'/'+ref  
                try:
                    r2 = requests.get(ref,timeout=8.0)
                except Exception as e:
                    print(news_name+':  '+str(type(e)))
                    errs.append(str(type(e)))
                    continue
                soup2 = bs(r2.content,"lxml")
                article=""
                for words in soup2.find_all("p"):
                    article+= unicode(words.string).encode("utf-8")
                    #link.get("a")
                if len(article)<1284:
                    continue
                arts.append(article)
                country.append(state)
                art_links.append(site+ref)
                name_news.append(news_name)
                try:
                    summary.append(unicode(link.string).encode("utf-8"))
                except TypeError:
                    summary.append(unicode(link.span.string).encode("utf-8")) 
    if i==2:
        print 'Completed one run'
#g_data = soup.find_all("div",{"class": "info"})
data={'site':name_news,'articles':arts,'Titles':summary,'Links':art_links, 'Time_Stamp':stamp,'Errors':errs,'Country':country}
pickle_loc=open(r'articleslinkstitle'+stamp+'.pickle',"wb")
sites=pickle.dump(data,pickle_loc)
pickle_loc.close()
print( 'Found '+str(len(data['articles']))+' articles')
