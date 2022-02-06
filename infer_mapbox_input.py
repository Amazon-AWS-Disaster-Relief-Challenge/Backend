# python 2
import requests
import json 
import argparse
import math 

model_id = 2
tile_size = 500
osm_only=0
output="out.json"

def execute_script(lat, lon):
    msg = {}
    msg["lat"] = float(lat)
    msg["lon"] = float(lon)
    msg["v_thr"] = 0.05
    msg["e_thr"] = 0.01
    msg["snap_dist"] = 15
    msg["snap_w"] = 100
    msg["model_id"] = model_id

    msg["size"] = tile_size;
    n = int(math.ceil(tile_size / 176.0))
    msg["padding"] = (n * 176 - tile_size)//2;
    msg["stride"] = 176;
    msg["nPhase"] = 1;
    if model_id == 3:
        msg["nPhase"] = 5;
    
    if osm_only != 0:
        msg["osm"] = True

    url = "http://sat2graph:8001"

    x = requests.post(url, data = json.dumps(msg))
    graph = json.loads(x.text) 
    if graph["success"] == 'false':
        print("unknown error")
        return "Some error Occured"

    print(graph)
    
    if osm_only != 0:
        json.dump(graph["osmgraph"], open(output, "w"), indent=2)
    else:
        json.dump(graph["graph"]["graph"][0], open(output, "w"), indent=2)
    
    tid = graph["taskid"]
    print("please check intermediate results at http://sat2graph:8010/t%d/" % tid)
    return [tid, graph["graph"]["graph"][0]]
