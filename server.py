from cmath import exp
import imp
import mercantile
import requests
from flask import Flask
from flask import request
from infer_mapbox_input import execute_script
import shutil as sh
import os
import json
import subprocess


app = Flask(__name__)

def getImageMapBox(latitude, longitude):
    MAPBOX_PUBLIC_KEY = "pk.eyJ1Ijoicm9oaXRqYWluMDAiLCJhIjoiY2t6OHRpYXM3MTd1ZDJwcW51M2xsamxkZyJ9.y2T27Pnd-g2fdCSZljvJlg"
    got_pre_disaster_image = False
    got_post_disaster_image = False

    delta = 0.02
    zoom = 15

    min_latitude = latitude - delta
    max_latitude = latitude + delta
    min_longitude = longitude - delta
    max_longitude = longitude + delta

    upper = mercantile.tile(min_longitude, max_latitude, zoom)
    lower = mercantile.tile(max_longitude, min_latitude, zoom)

    x_tile_range = [upper.x, lower.x]
    y_tile_range = [upper.y, lower.y]
    print("x_tile_range = ", x_tile_range)
    print("y_tile_range = ", y_tile_range)

    x = upper.x
    y = upper.y

    r = requests.get(
        f"https://api.mapbox.com/v4/mapbox.satellite/{zoom}/{x}/{y}@2x.png?access_token={MAPBOX_PUBLIC_KEY}", 
        stream=True
    )
    if r.status_code == 200:
        got_pre_disaster_image = True
        with open(f"./pre_disaster.png", "wb") as f:
            r.raw.decode_content = True
            sh.copyfileobj(r.raw, f)
    else:
        print("[ERROR]: Pre Disaster Response: ", r)
    
    # Post Disaster
    r = requests.get(
        f"https://api.mapbox.com/v4/jackkwok.digitalglobe_harvey_3020132_tif/{zoom}/{x}/{y}@2x.png?access_token={MAPBOX_PUBLIC_KEY}", 
        stream=True
    )
    if r.status_code == 200:
        got_post_disaster_image = True
        with open(f"./post_disaster.png", "wb") as f:
            r.raw.decode_content = True
            sh.copyfileobj(r.raw, f)
    else:
        print("[ERROR]: Post Disaster Response: ", r)
                
    if got_pre_disaster_image and not got_post_disaster_image:
        raise ValueError("Incompatible Latitude and Longitude. Try a different location")
    
@app.route('/', methods=['GET'])
def hello():
    lat = float(request.args.get('lat'))
    long = float(request.args.get('lon'))
    if not lat or not long:
        return "No lat long provided"
    print('Starting execution')
    o = execute_script(lat, long)
    # outJson, tid = get_outJson(getImageMapBox(lat, long))
    # getImageMapBox(lat, long)
    # cmd = "python infer_custom_input.py -input pre_disaster.png -gsd 0.5 -model_id 2 -output out.json"
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # out, err = p.communicate() 
    # p.wait()
    # print('execution complete ', out.decode('utf-8'))
    # print(err)
    try:
        # outJson = json.load(open('out.json'))
        # return json.dumps(outJson)
        return {
            "tid": o[0],
            "out": o[1]
        }
    except:
        return "Unable to get out.json"


if __name__ == "__main__":
	app.run(host ='0.0.0.0', port = 5001, debug = True)
