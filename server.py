import re
from flask import Flask
from flask import request
from infer_mapbox_input import execute_script

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    lat = request.args.get('lat')
    long = request.args.get('lon')
    if not lat or not long:
        return "No lat long provided"
    print('Starting execution')
    tid = execute_script(lat, long)
    print('execution complete')
    return { "tid" : tid}


if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5001, debug = True)
