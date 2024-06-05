from flask import Flask, request
from flask import jsonify
from scapy.all import *
import json
from pymongo import MongoClient
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import glob
import joblib

from pyflowmeter.sniffer import create_sniffer
from scapy.all import conf
import hashlib

import numpy as np
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler

from pathlib import Path
import pandas as pd

COLUMNS_ORDER = []
print("hello")
COLUMNS_ORDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'columns_order.json')
with open(COLUMNS_ORDER_PATH) as f:
    COLUMNS_ORDER = json.load(f)

MODEL_DIR_PATH = "C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Models"
CURRENT_MODEL_NAME = "001_dense"
COLUMNS_DICT = {
    "Destination Port":'dst_port',
    "Flow Duration":'flow_duration',
    "Total Fwd Packets":'tot_fwd_pkts',
    "Total Backward Packets":'tot_bwd_pkts',
    "Total Length of Fwd Packets":'totlen_fwd_pkts',
    "Total Length of Bwd Packets":'totlen_bwd_pkts',
    "Fwd Packet Length Max":'fwd_pkt_len_max',
    "Fwd Packet Length Min":'fwd_pkt_len_min',
    "Fwd Packet Length Mean":'fwd_pkt_len_mean', 
    "Fwd Packet Length Std":'fwd_pkt_len_std',
    "Bwd Packet Length Max":'bwd_pkt_len_max',
    "Bwd Packet Length Min":'bwd_pkt_len_min',
    "Bwd Packet Length Mean":'bwd_pkt_len_mean',
    "Bwd Packet Length Std":'bwd_pkt_len_std', 
    "Flow Bytes/s":'flow_byts_s',
    "Flow Packets/s":'flow_pkts_s',
    "Flow IAT Mean":'flow_iat_mean',
    "Flow IAT Std":'flow_iat_std',
    "Flow IAT Max":'flow_iat_max',
    "Flow IAT Min":'flow_iat_min',
    "Fwd IAT Total":'fwd_iat_tot',
    "Fwd IAT Mean":'fwd_iat_mean',
    "Fwd IAT Std":'fwd_iat_std',
    "Fwd IAT Max":'fwd_iat_max',
    "Fwd IAT Min":'fwd_iat_min',
    "Bwd IAT Total":'bwd_iat_tot',
    "Bwd IAT Mean":'bwd_iat_mean',
    "Bwd IAT Std":'bwd_iat_std',
    "Bwd IAT Max":'bwd_iat_max',
    "Bwd IAT Min":'bwd_iat_min',
    "Fwd PSH Flags":'fwd_psh_flags',
    "Bwd PSH Flags":'bwd_psh_flags',
    "Fwd URG Flags":'fwd_urg_flags',
    "Bwd URG Flags":'bwd_urg_flags',
    "Fwd Header Length":'fwd_header_len',
    "Bwd Header Length":'bwd_header_len',
    "Fwd Packets/s":'fwd_pkts_s',
    "Bwd Packets/s":'bwd_pkts_s',
    "Min Packet Length":'pkt_len_min',
    "Max Packet Length":'pkt_len_max',
    "Packet Length Mean":'pkt_len_mean',
    "Packet Length Std":'pkt_len_std',
    "Packet Length Variance":'pkt_len_var', 
    "FIN Flag Count":'fin_flag_cnt', 
    "SYN Flag Count":'syn_flag_cnt',
    "RST Flag Count":'rst_flag_cnt',
    "PSH Flag Count":'psh_flag_cnt',
    "ACK Flag Count":'ack_flag_cnt',
    "URG Flag Count":'urg_flag_cnt',
    "CWE Flag Count":'cwe_flag_count',
    "ECE Flag Count":'ece_flag_cnt',
    "Down/Up Ratio":'down_up_ratio',
    "Average Packet Size":'pkt_size_avg',
    "Avg Fwd Segment Size":'fwd_seg_size_avg',
    "Avg Bwd Segment Size":'bwd_seg_size_avg',
    "Fwd Header Length.1":'fwd_header_len',
    "Fwd Avg Bytes/Bulk":'fwd_byts_b_avg',
    "Fwd Avg Packets/Bulk":'fwd_pkts_b_avg',
    "Fwd Avg Bulk Rate":'fwd_blk_rate_avg',
    "Bwd Avg Bytes/Bulk":'bwd_blk_rate_avg',
    "Bwd Avg Packets/Bulk":'bwd_pkts_b_avg',
    "Bwd Avg Bulk Rate":'bwd_blk_rate_avg',
    "Subflow Fwd Packets":'subflow_fwd_pkts',
    "Subflow Fwd Bytes":'subflow_fwd_byts',
    "Subflow Bwd Packets":'subflow_bwd_pkts',
    "Subflow Bwd Bytes":'subflow_bwd_byts',
    "Init_Win_bytes_forward":'init_fwd_win_byts',
    "Init_Win_bytes_backward":'init_bwd_win_byts',
    "act_data_pkt_fwd":'fwd_act_data_pkts',
    "min_seg_size_forward":'fwd_seg_size_min',
    "Active Mean":'active_mean',
    "Active Std":'active_std',
    "Active Max":'active_max',
    "Active Min":'active_min',
    "Idle Mean":'idle_mean',
    "Idle Std":'idle_std',
    "Idle Max":'idle_max',
    "Idle Min":'idle_min'}
MODEL = None

def load_label_encoder():
    PROCESSED_DIR_PATH = 'C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Preprocess'
    le_classes = np.load(os.path.join(PROCESSED_DIR_PATH, 'label_encoder.npy'), allow_pickle=True)
    le = LabelEncoder()
    le.classes_ = le_classes
    return le

def load_scaler():
    PROCESSED_DIR_PATH = 'C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Preprocess'
    return joblib.load(os.path.join(PROCESSED_DIR_PATH, 'scaler.gz'))

SCALER = load_scaler()
LE = load_label_encoder()

def create_connection(dev_id):
    client = MongoClient('127.0.0.1', 27017)
    mydb = client['PacketStoreDB']
    collection_name = 'PacketStoreCollection'+str(dev_id)
    collection = []
    if collection_name not in mydb.list_collection_names():
        collection = mydb[collection_name]
    collection = mydb[collection_name]
    return collection

def GET_MODELS():
    file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Models', '*.h5')
    models = [Path(os.path.basename(model)).stem for model in glob.glob(file_dir)]
    return models


def LOAD_MODEL(model_name):
    global MODEL
    global CURRENT_MODEL_NAME
    if model_name in GET_MODELS():
        model_path = os.path.join(MODEL_DIR_PATH, model_name+'.h5')
        #MODEL = tf.keras.saving.load_model(model_path)
        MODEL = tf.keras.models.load_model(model_path)
        CURRENT_MODEL_NAME = model_name
        return True
    return False

LOAD_MODEL(CURRENT_MODEL_NAME)

TIMEOUT_UPDATE = 10
SENDING_INTERVAL = 5
PAGE_SIZE = 50
MONITORING_THREADS = {}
SERVER_ENDPOINT='http://127.0.0.1:7778/endpoint_ex'


def preprocessing(df: pd.DataFrame, useOld=True):
 
    x = df.iloc[:, df.columns != 'Label']
    PROCESSED_DIR_PATH = 'C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Preprocess'
    if useOld:
        scaler = joblib.load(os.path.join(PROCESSED_DIR_PATH, 'scaler.gz'))
        x = scaler.transform(x)
    else:
    # Scale the features between 0 ~ 1
        scaler = MinMaxScaler()
        x = scaler.fit_transform(x)
        joblib.dump(scaler, os.path.join(PROCESSED_DIR_PATH, 'scaler.gz'))

    return x

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


@app.route('/start_analyze', methods=['GET','POST'])
def start_analyze():
    dev_id = request.args['dev_id']
    collection = create_connection(dev_id=dev_id)
    flows =  list(collection.find({}))
    rflows = []
    for flow in flows:
        rflow = {}
        for key, val in COLUMNS_DICT.items():
            rflow[key] = flow[val]
        rflows.append(rflow)
    df = pd.DataFrame(rflows)
    x = preprocessing(df)
    y_pred = MODEL.predict(x, batch_size=1024, verbose=False)
    y_pred = np.argmax(y_pred, axis=1)
    y_pred = LE.inverse_transform(y_pred)
    response = jsonify({'y_pred':y_pred.tolist()})
    i = 0
    for flow in flows:
        collection.update_one({'_id':flow['_id']}, { "$set":{CURRENT_MODEL_NAME:y_pred[i]}})
        i+=1
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/clear_analyze', methods=['GET','POST'])
def clear_analyze():
    dev_id = request.args['dev_id']
    collection = create_connection(dev_id=dev_id)
    flows =  list(collection.find({}))
    for flow in flows:
        collection.update_one({'_id':flow['_id']}, { "$unset":{CURRENT_MODEL_NAME:1}})
    response = jsonify({'STATUS':'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_flows', methods=['GET'])
def get_flows():
    dev_id = request.args['dev_id']
    collection = create_connection(dev_id=dev_id)
    flows =  list(collection.find({}, {"_id":False}))
    response = jsonify({'data':flows} )
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


@app.route('/is_monitoring', methods=['GET'])
def is_monitoring():
    args = request.args
    dev_id = args['dev_id']
    response = jsonify({"is_monitoring":dev_id in MONITORING_THREADS.keys()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





print("Сервер запущен")
if __name__ == '__main__':
    app.run(debug=True, port=7778)