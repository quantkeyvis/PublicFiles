import pandas as pd 
import numpy as np 
import os
import sys
import folium
import json
import requests
import geopandas 
import hvplot
import vincent


m = folium.Map(location=[39.381266,-97.922211], zoom_start=5.3)
sts="/districts/states/"
# sts should point to a directory of http://github.com/unitedstates/districts
for subdir, dirs, files in os.walk(sts):
	if len(dirs)>3:
		for state in dirs:
			if len(state)<3:
				folium.GeoJson(sts+state+"/shape.geojson", name="geojson "+state).add_to(m)
				print(state)
				for subdir, dirs, files in os.walk(sts+state+"/sldu/"):
					#print(files)
					for file in files:
						folium.GeoJson(sts+state+"/sldu/"+file, name="geojson "+state+"-"+file.split('.')[0]).add_to(m)

m.save(outfile='datamap.html')
