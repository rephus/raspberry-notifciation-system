#!/usr/bin/python
import time
from db.readings import Readings
from services.network import Network
from flask import Flask, jsonify, render_template, request #http://flask.pocoo.org/
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.cfg")

nmap_enabled = config.getboolean('network','nmap_enabled')
network = Network(nmap_enabled)
readings = Readings()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/graphs")
def graphs():
    return render_template('graphs.html')
  
@app.route("/readings/last")
def readings_last():
    start = time.time()
    json = []
    
    for device in readings.devices:
      read = readings.last(device)
      timestamp = read[1]
      value = read[2]
      
      json.append({
        "id": read[0],
        "time":  read[1],
        "value":  read[2],
        "device": device
      })
      
    return jsonify({
      "results":json,
      "time": int(time.time()- start)
    })
  
@app.route("/readings/all")
def readings_all():
    limit = request.args.get('l')
    start = time.time()
    read = readings.all(limit)
    print "Parsing {} actions".format(len(read))
    json = []
    for a in read:
      j = {
        "id": a[0],
        "timestamp": a[1],
        "value": a[2],
        "device": a[3]
      }
      json.append(j)
      
    return jsonify({
      "count":len(json), 
      "results":json,
      "time": int(time.time()- start)
    })
  
@app.route("/home")
def home():
    start = time.time()
    json = []
    
    #Search by mac
    '''
    for phone in config.items("macs"):
      name = phone[0]
      mac = phone[1]
      device =  network.get(mac)
      if device is None: status= "unreachable"
      elif device.is_up(): status="on"
      else: status="off"
      
      json.append({
        "name": name,
        "mac":  mac,
        "status":  status
      })
    '''
    #Search by private ip
    for phone in config.items("ips"):
      name = phone[0]
      ip = phone[1]
      device =  network.get_ip(ip)
      if device is None: status= "unreachable"
      else: status="on"
      
      json.append({
        "name": name,
        "mac":  ip,
        "status":  status
      })
    
    return jsonify({
      "results":json,
      "time": int(time.time()- start)
    })
  
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001, debug = True)
    
def empty_home():
  for mac in macs:
    device =  network.get(mac)
    if device is not None and device.is_up(): return False
  return True
