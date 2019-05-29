import pandas as pd
import random
import uuid

states=['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']


state_name=pd.read_csv('/home/tacticalforesight/Documents/gitH/TF_Storage/Tactical Foresight/Pro Bono/Campaign Finance/State_Abbrev.csv',index_col=1)
print('state_name')
print(state_name.columns)
print('\n')
state_income=pd.read_csv('/home/tacticalforesight/Documents/gitH/TF_Storage/Tactical Foresight/Pro Bono/Campaign Finance/State_Income.csv',index_col=0)
print('state_income')
print(state_income.columns)
print('\n')
state_affil=pd.read_csv('/home/tacticalforesight/Documents/gitH/TF_Storage/Tactical Foresight/Pro Bono/Campaign Finance/State_Party.csv',index_col=0)
print('state_affil')
print(state_affil.columns)
print('\n')
print(state_income.index)
print('\n')
gold_contributor_rec={'Ballot_Measure':0,'State_Of_Contrbutor':0, 'Amount':0, 'contributor_party':0 , 'Individual_Or_Corp':0, 'Contributor_Name':0}
gold_ballot_rec={'Ballot_Measure':0,'State_Of_Ballot':0, 'Party_Support':0, 'State_Party':0,'State_Party_Percent':0,'State_Median_Income':0, 'Passed':0}
ballots={}
contributors={}
for i in range(50000):
	rec=dict(gold_ballot_rec)
	rec['Ballot_Measure']=uuid.uuid4()
	rec['State_Of_Ballot']= random.choice(states)
	rec['Party_Support']=random.choice(['Democratic','Republican','Other'])
	rec['Other_Party'] = random.choice(list(set(['Democratic','Republican','Other'])-set([rec['Party_Support']])))
	state=state_name.loc[rec['State_Of_Ballot'],'State'].title()
	rec['State_Party']=state_affil.loc[state,'Party']
	rec['State_Party_Percent']=float(state_affil.loc[state, 'Party_Percent'])
	rec['State_Median_Income']=float(state_income.loc[state, 'Median household income'].replace('$','').replace(',',''))
	contributors[rec['Ballot_Measure']]=[]
	sc=random.random()
	cp=random.random()
	st=random.random()
	for j in range(random.choice(range(1000,10000))):
		contrib=dict(gold_contributor_rec)
		contrib['Contributor_Name']=uuid.uuid4()
		contrib['Ballot_Measure']=rec['Ballot_Measure']
		contrib['State_Of_Contrbutor']= rec['State_Of_Ballot'] if rec['Party_Support']!=rec['State_Party'] and random.random()<st  else random.choice(states)
		contrib['State_Of_Contrbutor']= rec['State_Of_Ballot'] if rec['Party_Support']==rec['State_Party'] and random.random()<0.8 else contrib['State_Of_Contrbutor']
		contrib['contributor_party']=rec['Other_Party'] if contrib['State_Of_Contrbutor']!=rec['State_Of_Ballot'] else rec['State_Party']
		if rec['State_Party']==contrib['contributor_party']:
			if rec['Party_Support']!=rec['State_Party']:
				if sc<random.random():
					contrib['contributor_party']=rec['State_Party']
				else:
					contrib['contributor_party']=rec['Other_Party']
			else:
				contrib['contributor_party']=rec['Other_Party'] if rec['State_Party_Percent']+0.1<=random.random() else rec['State_Party']
		if cp<0.5:
			if random.random()>0.85:
				contrib['Individual_Or_Corp']='Corp'
			else:
				contrib['Individual_Or_Corp']='Individual'
		else:
			if random.random()>0.99:
				contrib['Individual_Or_Corp']='Corp'
			else:
				contrib['Individual_Or_Corp']='Individual'
		if contrib['Individual_Or_Corp']=='Corp':
			amount=random.random()*2000000
		else:
			amount=random.random()*15000
		contrib['Amount']=amount
		contributors[rec['Ballot_Measure']].append(contrib)
	contr_data=pd.DataFrame(contributors[rec['Ballot_Measure']])
	#Pickup
	pvs=sum(contr_data[contr_data['Individual_Or_Corp']=='Corp']['Amount'])/float(state_income.loc[state, 'population'])
	rec['Corp_Count']=pvs
	rec['pop_percent_contrib'] = contr_data.shape[0]/float(state_income.loc[state, 'population'])
	rec['foreign_influence_ration']= sum(contr_data[contr_data['State_Of_Contrbutor']==rec['State_Of_Ballot']]['Amount'])/(1.0+sum(contr_data[contr_data['State_Of_Contrbutor']!=rec['State_Of_Ballot']]['Amount']))
	print(sum(contr_data[contr_data['State_Of_Contrbutor']==rec['State_Of_Ballot']]['Amount']))
	print(sum(contr_data[contr_data['State_Of_Contrbutor']!=rec['State_Of_Ballot']]['Amount']))
	print('per voter spend of {}'.format(pvs))
	print(contr_data.shape[0]/float(state_income.loc[state, 'population']))
	if rec['Party_Support']==rec['State_Party']:
		if rec['State_Party_Percent']>=0.7:
			passed= 1 if random.random()>0.1 else 0
		else:
			if pvs<20:
				passed = 0 if random.random()>0.3 else 1
			else:
				passed = 1 if random.random()>0.3 else 0
	else:
		if rec['State_Party_Percent']<0.7:
			if contr_data.shape[0]/float(state_income.loc[state, 'population'])>0.001:
				passed = 1 if random.random()>0.3 else 0
			else:
				passed= 0 if random.random()>0.3 else 1
		else:
			#Assume info got out about 'foreign' influence and the voters did not like that
			if rec['foreign_influence_ration']>=2:
				#Assume wealthier voters are more adventurous voters
				if rec['State_Median_Income']>58000:
					portion=0.2
				else:
					portion=0.6
				passed = 1 if random.random()>portion else 0
			else:
				passed = 0 if random.random()>0.3 else 1
	rec['Passed']=passed
	print('Passed: {}'.format(passed))
	if i%100==0:
		print(i)
	print('\n\n')
	ballots[rec['Ballot_Measure']]=rec
	contributors[rec['Ballot_Measure']]='done'
ballots=pd.DataFrame([i for i in ballots.values()])
ballots.to_csv('/home/tacticalforesight/Desktop/Tactical Foresight/Pro Bono/Campaign Finance/Data/pseudo_ballots.csv')
d=[]
sys.exit()
for recs in contributors.values():
	d.extend(recs)
contr=pd.DataFrame(d)
contr.to_csv('/home/tacticalforesight/Desktop/Tactical Foresight/Pro Bono/Campaign Finance/Data/pseudo_contributors.csv')

result = pd.merge(contr, ballots, on='Ballot_Measure')
print(result.head())
result.to_csv('/home/tacticalforesight/Desktop/Tactical Foresight/Pro Bono/Campaign Finance/Data/pseudo_ballot_contrib_influence.csv')