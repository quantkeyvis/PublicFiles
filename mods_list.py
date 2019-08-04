import pkgutil


mods=[str(x) for x in pkgutil.iter_modules()]
for m in mods:
	if 'CoreNLP_Last_it_corrupt' in m or 'pydpc' in m:
		print(m)

cln=[x.split("name='")[1] for x in mods if "FileFinder('/home/tacticalforesight/Documents/gitH/TF_Storage/py scripts')" not in x]
cln=[x.split("',")[0] for x in cln]

with open('all_mods.txt','w') as file:
	for mod in cln:
		file.write("%s\n" % mod)
print('done\n\n\n')
print(mods)
