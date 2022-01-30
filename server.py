import re
from flask import Flask
from flask import request
from Sat2Graph.docker.scripts.infer_mapbox_input import execute_script

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    lat = request.args.get('lat')
    long = request.args.get('lon')
    if not lat or not long:
        return "No lat long provided"
    print('Starting execution')
    print(execute_script(lat, long))
    print('execution complete')
    ret_string = lat + ' : ' + long
    return ret_string


if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5001, debug = True)
