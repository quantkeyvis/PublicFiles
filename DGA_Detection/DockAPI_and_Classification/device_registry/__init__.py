from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import markdown
import os
import DGA_Class
import re
#import sklearn

print(re.sub(r'(est)$','esting done!','test'))
# The Restful API is based on the following github repo: https://github.coFROM python:3
"""
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]m/home/tacticalforesight/Desktop/secureworks/device_registry
"""

#Create Flask instance
app= Flask(__name__)

# Create the API
api = Api(app)

@app.route("/")
def index():
    #return "Hello World - Start Detecting DGAs!"
    
    # Open readme file
    with open(os.path.dirname(app.root_path)+'/README.md', 'r') as markdown_file:
        #Read Content
        content = markdown_file.read()
        
        #Convert to HTML
        return markdown.markdown(content)

    
class DGA_Ind(Resource):
    def get(self, identifier):
        try:
            site_type=DGA_Class.classify(identifier)
            return {'message': 'Site Type Inferred', 'data': site_type}, 200
        except Exception as err:
            return {'message': 'Error in classification: \n'+str(err), 'data': 'N/A'}, 404




api.add_resource(DGA_Ind,'/device/<string:identifier>')