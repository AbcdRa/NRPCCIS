from flask import Flask, request
from flask import jsonify
from scapy.all import *
import json
from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps

import os
from os import listdir
from os.path import isfile, join
import glob

from tensorflow.python import keras
import pandas as pd
from pyflowmeter.sniffer import create_sniffer
from scapy.all import conf
import hashlib

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler

COLUMNS_ORDER = []
print("hello")
COLUMNS_ORDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'columns_order.json')
with open(COLUMNS_ORDER_PATH) as f:
    COLUMNS_ORDER = json.load(f)

MODEL_DIR_PATH = "C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Models"
CURRENT_MODEL_NAME = "08_cnn.h5"

MODEL = None

def GET_MODELS():
    file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Models', '*.h5')
    models = [os.path.basename(model) for model in glob.glob(file_dir)]
    return models


def LOAD_MODEL(model_name):
    global MODEL
    global CURRENT_MODEL_NAME
    if model_name in GET_MODELS():
        MODEL = tf.keras.models.load_model(os.path.join(MODEL_DIR_PATH, model_name))
        CURRENT_MODEL_NAME = model_name
        return True
    return False

LOAD_MODEL('08_cnn.h5')

TIMEOUT_UPDATE = 10
SENDING_INTERVAL = 5
PAGE_SIZE = 50
MONITORING_THREADS = {}
SERVER_ENDPOINT='http://127.0.0.1:7778/endpoint_ex'

def preprocess_x(raw_X: list[dict]) -> np.ndarray:
    scaler = MinMaxScaler()
    X = np.zeros((len(raw_X), len(COLUMNS_ORDER)))
    i = 0
    for raw_x in raw_X:
        for j, key in COLUMNS_ORDER:
            X[i][j] = raw_x[key]
    X = scaler.fit_transform(X)
    return X

def reshape_dataset_cnn(x: np.ndarray) -> np.ndarray:
    # Add padding columns
    result = np.zeros((x.shape[0], 81))
    result[:, :-3] = x

    # Reshaping dataset
    result = np.reshape(result, (result.shape[0], 9, 9))
    result = result[..., tf.newaxis]
    return result

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

@app.route('/get_models', methods=['GET'])
def get_models():
    models = GET_MODELS()
    response = jsonify(models)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/set_model', methods=['GET','POST'])
def set_models():
    args = request.args
    model_name = args['model_name']
    result = LOAD_MODEL(model_name)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_current_model', methods=['GET'])
def get_current_model():
    response = jsonify(CURRENT_MODEL_NAME)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict', methods=['GET','POST'])
def predict():
    flows = request.json['flows']
    x = preprocess_x(flows)
    x = reshape_dataset_cnn(x)
    y_pred = MODEL.predict(x, batch_size=1024, verbose=False)
    y_pred = np.argmax(y_pred, axis=1)
    response = jsonify({'STATUS':'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/train', methods=['GET','POST'])
def train():
    X = request.json['X']
    Y = request.json['Y']
    preX = preprocess_x(X)
    MODEL.fit(preX, Y, validation_split=0.1, epochs=10, batch_size=1024, verbose=True)
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
    collection = create_connection(dev_id=dev_id)
    flows =  list(collection.find({}, {"_id":False}))
    print(len(flows[0].keys()))
    response = jsonify({'data':flows})

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