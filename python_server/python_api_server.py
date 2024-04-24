from flask import Flask, request
from flask import jsonify
from scapy.all import *
import json
from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps
import pandas as pd
from pyflowmeter.sniffer import create_sniffer
from scapy.all import conf
import hashlib



TIMEOUT_UPDATE = 10
SENDING_INTERVAL = 5
PAGE_SIZE = 50
MONITORING_THREADS = {}
SERVER_ENDPOINT='http://127.0.0.1:7778/endpoint_ex'

app = Flask(__name__)

@app.route('/get_ifaces')
def get_ifaces():
    ifs = [{'desc': i.description, 
            'index':i.index, 
            'mac':i.mac, 
            'ip4':i.ips[4], 
            'ip6':i.ips[6], 
            'is_mon': str(i.index) in MONITORING_THREADS.keys()} 
            for i in conf.ifaces.data.values()]

    response = jsonify(ifs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/endpoint_ex', methods=['GET','POST'])
def endpoint_ex():
    dev_id = conf.ifaces.dev_from_networkname(request.json['input_interface']).index
    flows = request.json['flows']
    collection = create_connection(dev_id)
    
    for flow in flows:
        hexdigest = hashlib.md5(json.dumps(flow, sort_keys=True).encode('utf-8')).hexdigest()
        try:
            collection.insert_one({'id':hexdigest, 'created_time':time.mktime(datetime.now().timetuple()), **flow})
        except UnicodeEncodeError:
            print(flow)

    response = jsonify({'STATUS':'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_flows', methods=['GET'])
def get_flows():
    args = request.args
    dev_id = args['dev_id']
    page = 0
    try:
        page = args['page']
    except KeyError: pass
    print(page)
    collection = create_connection(dev_id=dev_id)
    response = jsonify(dumps(collection.find({})))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/start_monitoring', methods=['GET'])
def start_monitoring():
    args = request.args
    dev_id = args['dev_id']
    if dev_id in MONITORING_THREADS.keys() and MONITORING_THREADS[dev_id].running:
        response = jsonify({"result":"Already Monitoring"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    sniffer = create_sniffer(
            input_interface=conf.ifaces.dev_from_index(int(dev_id)).network_name,
            server_endpoint=SERVER_ENDPOINT,
            verbose=True,
            sending_interval=SENDING_INTERVAL
        )
    sniffer.start()
    MONITORING_THREADS[dev_id] = sniffer
    response = jsonify({"result":"Start Monitoring"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/stop_monitoring', methods=['GET'])
def stop_monitoring():
    args = request.args
    dev_id = args['dev_id']
    if dev_id in MONITORING_THREADS.keys():
        try:
            MONITORING_THREADS[dev_id].stop()
        except scapy.error.Scapy_Exception:
            pass
        MONITORING_THREADS[dev_id].join()
        del MONITORING_THREADS[dev_id]
    response = jsonify({"result":"Stop Monitoring"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def create_connection(dev_id):
    client = MongoClient('127.0.0.1', 27017)
    collection = client['PacketStoreDB']['PacketStoreCollection'+str(dev_id)]
    return collection


print("Сервер запущен")
if __name__ == '__main__':
    app.run(debug=True, port=7778)