# -*- coding: utf-8 -*-
import spacy
import en_core_web_sm as en_core
import pickle
import csv
import math
import json
import sys
import re
import datetime
import nltk 


extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e']
sent_tokenize = nltk.data.load('tokenizers/punkt/english.pickle')
sent_tokenize._params.abbrev_types.update(extra_abbreviations)

pickle_loc=open(r'\articles\articleslinkstitle'+'2017-11-09'+'.pickle',"rb")
sites=pickle.load(pickle_loc)
pickle_loc.close()


#nlp = spacy.load('en')
nlp=en_core.load()
print 'start'
doc = nlp(u'I like green eggs and ham.')
i=0
tex=u'Rick, the red dog, waited for hours to run around the small dog of the corn, before the midnight heat in arizona.'
doc=nlp(tex)
verbs = []
start=datetime.datetime.now()
from spacy.symbols import nsubj, VERB
for possible_verb in doc:
        for possible_subject in possible_verb.children:
                print(possible_subject,[i for i in possible_subject.ancestors])
                print([i for i in possible_subject.children])
                if possible_subject.dep == nsubj:
                        verbs.append(possible_verb)
                        end=datetime.datetime.now()
                        dif_time=end-start
                        print(dif_time)
                        print(possible_verb)
                        break

print('\n\n\n\n\n')

viz_deps=[('word text','word position', 'dependency type', 'dependency head position')]
d3_viz={"nodes":[],"links":[]}
nodes_place={}
for jp,word in enumerate(doc):
        nodes_place[word.text]=jp
for jp,word in enumerate(doc):
        #print(word.i, word.dep_, word.head.i,word.iob)
        #print(word.text,word.pos_, math.exp(word.prob), word.dep_, word.head.text)
        if word.text==',':
                viz_deps.append(('punct',word.i, word.dep_, word.head.i))
                d3_viz["nodes"].append({"name":"comma", "group":word.pos})
                d3_viz["links"].append({"source":jp, "target":nodes_place[word.head.text],"weight":round(math.exp(word.prob)*100,4)+0.0001, "type":word.dep_})
                nodes_place[word.text]=jp
        else:
                viz_deps.append((word.text,word.i, word.dep_, word.head.i))
                d3_viz["nodes"].append({"name":word.text, "group":word.pos})
                d3_viz["links"].append({"source":jp, "target":nodes_place[word.head.text],"weight":round(math.exp(word.prob)*100,4)+0.0001, "type":word.dep_})
                nodes_place[word.text]=jp
##for i in xrange(len(doc)):
##    print(doc[i].text, doc[i].pos_, doc[i].ent_iob, doc[i].ent_type_)

stop_codec=[u'\xd2',u'\xe0',u'\u2011',u'\ude31',u'\ude0d',u'\ud83d',u'\u05d3',u'\u05de',u'\u05d7',u'\u202c',u'\xe4',u'\xf6',u'\u2013',u'\xf3',u'\xeb',u'\xad',u'\xf4'
            ,u'\u2014',u'\u0302',u'\u200b',u'\xa9',u'\xc9',u'\xed',u'\xfc',u'\xc1',u'\xd6',u'\U0001f9c0',u'\u2013',u'\xe8',u'\u20ac',u'\u2022',u'\u2026',u'\xe1'
            ,u'\xf1',u'\xfa',u'\xe7',u'\xa3',u'\xef','\xa0',u'\u2019',u'\xe9',u'\u201c',u'\u201d',u'0xc3',u'\u2018',u'\u0131',u'\u011f',u'\u015f',u'\u0159',u'\u0101'
            ,u'\u0161',u'\u0301',u'\xbf',u'\xe1',u'\ufffd',u'\u20b9']
fix_codec=[(0, "O"),(1, "a"),(2, "-"),(3, "-"),(4, "-"),(5, "-"),(6, "-"),(7, "n"),(8, "tau"),(9,"-"),(10, "a"),(11, "o"),(12, "-"),(13, "o"),(14, "e"),(15, "-"),(16, "o"),(17, "-"),(18, "^"),(19, "-"),(20, "copywritten"),(21, "E"),(22, "i"),(23, "u"),(24, "A"),(25, "o"),(26, ""),(27, "-"),(28, "e"),(29, "yen"),(30, "-"),(31, "..."),(32, "a"),(33, "n"),(34, "u"),(35, "c"),(36, "euro"),(37, 'l'),(38, " "),(39, "'"),(40, 'e'),(41, '"'),(42, '"'),(43, "0c3"),(44, "'"),(45, 'l'),(46, 'g'),(47, 's'),(48, 'r'),(49, "a"),(50, "s"),(51,"'"),(52, "?"),(53, "a"),(54, "?"),(55, "yen")]
codec={}
for i in fix_codec:
        codec[stop_codec[i[0]]]=i[1]
def conell2009(doc):
        text=''
        for i,word in enumerate(doc):
                text+=str(i+1)+'\t'+word.text+'\t'+'_'+'\t'+word.lemma_+'\t'+'_'+'\t'
                if str(i+1)==str(word.head.i+1):
                        text+=word.pos_+'\t'+'_'+'\t'+'_'+'\t'+str(-1)+'\t'+str(0)+'\t'+'_'+'\t'+word.dep_+'\t'+'_'+'\t'+'_'
                else:
                        text+=word.pos_+'\t'+'_'+'\t'+'_'+'\t'+str(-1)+'\t'+str(word.head.i+1)+'\t'+'_'+'\t'+word.dep_+'\t'+'_'+'\t'+'_'
                text+='\n'
        return text
all_dep=[u'ROOT',u'csubjpass', u'aux', u'punct', u'dobj', u'nmod', u'advmod', u'prep', u'amod', u'compound', u'pobj', u'nsubj', u'cc', u'appos', u'quantmod', u'npadvmod', u'xcomp', u'det', u'conj', u'dep', u'ccomp', u'intj', u'nsubjpass', u'auxpass', u'oprd', u'advcl', u'acl', u'nummod', u'relcl', u'mark', u'acomp', u'dative', u'poss', u'parataxis', u'expl', u'attr', u'agent', u'prt', u'neg', u'meta', u'prep||dobj', u'pcomp', u'pobj||prep', u'csubj', u'appos||nsubj', u'advmod||conj', u'nsubj||ccomp']
def dep_vec(docs):
        global all_dep,sent_tokenize
        global stop_codec
        global codec
        vec_hash=dict.fromkeys(all_dep,0)
        vec=[]
        for z,doc in enumerate(docs):
                vec_z=dict(vec_hash)
                doc=re.sub(u'0xc3',' ',unicode(doc))
                for i in stop_codec:
                        doc=re.sub(i,codec[i],doc)
                try:
                        for sent in sent_tokenize.tokenize(doc):
                                try:
                                        sent=unicode(sent)
                                except UnicodeDecodeError as err:
                                        print('UnicodeDecodeError')
                                        print sent
                                        print(err)
                                        print('\n\n')
                                        continue
                                pars = nlp(sent)
                                for i,word in enumerate(pars):
                                        try:
                                                vec_z[word.dep_]+=1
                                        except KeyError:
                                                print('New Found Dep: '+str(word.dep_))
                        vec.append(vec_z)
                except UnicodeDecodeError:
                        vec.append(dict(vec_hash))
        return vec
out_text=conell2009(doc)
dep_vec([i for i in sites['articles']])
print('done')
sys.exit()
with open(r'\textdep.txt', "w") as text_file:
    text_file.write(out_text)
text_file.close()
with open(r'\dddepsdata.json', 'w') as f:
     json.dump(d3_viz, f)

with open(r'\viz_deps.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in viz_deps:
            spamwriter.writerow(i)
