from os import listdir,getcwd
import subprocess
import sys
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>This is our Python Api!</h1>
<p>Run your python scripts remotely!</p>'''


@app.route('/piConnect/v1/scripts', methods=['GET'])
def retrieve_scripts():
    return jsonify(extractScripts())


@app.route('/piConnect/v1/runScript', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    scripts = extractScripts()
    cwd = getcwd()
    for script in scripts:
        if script['id'] == id:
	    print( cwd + "/" + script['name'])
            subprocess.call([sys.executable ,cwd + "/" + script['name']], shell=False)
            return "Ran Script: " + script['name']
    return "Failed to find script with Id:"+ id

def extractScripts():
    scripts = []
    cwd = getcwd()
    for idx,script in enumerate(listdir(cwd)):
        if(script == "api.py" or script[len(script)-3:len(script)] !=".py"):continue
        scripts.append(
            {
            'id':idx,
            'name':script
            }
        )
        print()
    print(scripts)
    return scripts

app.run(host='0.0.0.0', port=5000, debug=True)
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# So I basically need to do 3 things
# Create api to have a get. Retrieves names of all python scripts.
# Import files and functions
# Pass params in a string and parse them somehow. (Hardest Part)

