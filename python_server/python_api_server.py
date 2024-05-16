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

import tensorflow.keras as keras

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import plot_model


import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler


def preprocessing(df: pd.DataFrame) -> (np.ndarray, np.ndarray):
    # Shuffle the dataset
    df = df.sample(frac=1)

    # Split features and labels
    x = df.iloc[:, df.columns != 'Label']
    y = df[['Label']].to_numpy()

    # Scale the features between 0 ~ 1
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    return x, y


def preprocess_x(raw_x: dict) -> np.ndarray:
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    return x

def reshape_dataset_cnn(x: np.ndarray) -> np.ndarray:
    # Add padding columns
    result = np.zeros((x.shape[0], 81))
    result[:, :-3] = x

    # Reshaping dataset
    result = np.reshape(result, (result.shape[0], 9, 9))
    result = result[..., tf.newaxis]
    return result


def plot_history(history: tf.keras.callbacks.History):
    # summarize history for accuracy
    plt.plot(history.history['sparse_categorical_accuracy'])
    plt.plot(history.history['val_sparse_categorical_accuracy'])
    plt.title('model2 accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model2 loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def evaluation(model: keras.Model, x_test: np.ndarray, y_test: np.ndarray):
    score = model.evaluate(x_test, y_test, verbose=False)
    logging.info('Evaluation:\nLoss: {}\nAccuracy : {}\n'.format(score[0], score[1]))

    # F1 score
    y_pred = model.predict(x_test, batch_size=1024, verbose=False)
    y_pred = np.argmax(y_pred, axis=1)

    logging.info("\n{}".format(classification_report(y_test, y_pred)))


COLUMNS_ASS = [{'Destination Port': 'dst_port'},
 {'Flow Duration': 'flow_duration'},
 {'Total Fwd Packets': 'tot_fwd_pkts'},
 {'Total Backward Packets': 'tot_bwd_pkts'},
 {'Total Length of Fwd Packets': 'totlen_fwd_pkts'},
 {'Total Length of Bwd Packets': 'totlen_bwd_pkts'},
 {'Fwd Packet Length Max': 'fwd_pkt_len_max'},
 {'Fwd Packet Length Min': 'fwd_pkt_len_min'},
 {'Fwd Packet Length Mean': 'fwd_pkt_len_mean'},
 {'Fwd Packet Length Std': 'fwd_pkt_len_std'},
 {'Bwd Packet Length Max': 'bwd_pkt_len_max'},
 {'Bwd Packet Length Min': 'bwd_pkt_len_min'},
 {'Bwd Packet Length Mean': 'bwd_pkt_len_mean'},
 {'Bwd Packet Length Std': 'bwd_pkt_len_std'},
 {'Flow Bytes/s': 'flow_byts_s'},
 {'Flow Packets/s': 'flow_pkts_s'},
 {'Flow IAT Mean': 'flow_iat_mean'},
 {'Flow IAT Std': 'flow_iat_std'},
 {'Flow IAT Max': 'flow_iat_max'},
 {'Flow IAT Min': 'flow_iat_min'},
 {'Fwd IAT Total': 'fwd_iat_tot'},
 {'Fwd IAT Mean': 'fwd_iat_mean'},
 {'Fwd IAT Std': 'fwd_iat_std'},
 {'Fwd IAT Max': 'fwd_iat_max'},
 {'Fwd IAT Min': 'fwd_iat_min'},
 {'Bwd IAT Total': 'bwd_iat_tot'},
 {'Bwd IAT Mean': 'bwd_iat_mean'},
 {'Bwd IAT Std': 'bwd_iat_std'},
 {'Bwd IAT Max': 'bwd_iat_max'},
 {'Bwd IAT Min': 'bwd_iat_min'},
 {'Fwd PSH Flags': 'fwd_psh_flags'},
 {'Bwd PSH Flags': 'bwd_psh_flags'},
 {'Fwd URG Flags': 'fwd_urg_flags'},
 {'Bwd URG Flags': 'bwd_urg_flags'},
 {'Fwd Header Length': 'fwd_header_len'},
 {'Bwd Header Length': 'bwd_header_len'},
 {'Fwd Packets/s': 'fwd_pkts_s'},
 {'Bwd Packets/s': 'bwd_pkts_s'},
 {'Min Packet Length': 'pkt_len_min'},
 {'Max Packet Length': 'pkt_len_max'},
 {'Packet Length Mean': 'pkt_len_mean'},
 {'Packet Length Std': 'pkt_len_std'},
 {'Packet Length Variance': 'pkt_len_var'},
 {'FIN Flag Count': 'fin_flag_cnt'},
 {'SYN Flag Count': 'syn_flag_cnt'},
 {'RST Flag Count': 'rst_flag_cnt'},
 {'PSH Flag Count': 'psh_flag_cnt'},
 {'ACK Flag Count': 'ack_flag_cnt'},
 {'URG Flag Count': 'urg_flag_cnt'},
 {'CWE Flag Count': 'cwe_flag_cnt'},
 {'ECE Flag Count': 'ece_flag_cnt'},
 {'Down/Up Ratio': 'down_up_ratio'},
 {'Average Packet Size': 'pkt_size_avg'},
 {'Avg Fwd Segment Size': 'fwd_seg_size_avg'},
 {'Avg Bwd Segment Size': 'bwd_seg_size_avg'},
 {'Fwd Header Length.1': 'fwd_header_len'},
 {'Fwd Avg Bytes/Bulk': 'fwd_byts_b_avg'},
 {'Fwd Avg Packets/Bulk': 'fwd_pkts_b_avg'},
 {'Fwd Avg Bulk Rate': 'fwd_blk_rate_avg'},
 {'Bwd Avg Bytes/Bulk': 'bwd_blk_rate_avg'},
 {'Bwd Avg Packets/Bulk': 'bwd_pkts_b_avg'},
 {'Bwd Avg Bulk Rate': 'bwd_blk_rate_avg'},
 {'Subflow Fwd Packets': 'subflow_fwd_pkts'},
 {'Subflow Fwd Bytes': 'subflow_fwd_byts'},
 {'Subflow Bwd Packets': 'subflow_bwd_pkts'},
 {'Subflow Bwd Bytes': 'subflow_bwd_byts'},
 {'Init_Win_bytes_forward': 'init_fwd_win_byts'},
 {'Init_Win_bytes_backward': 'init_bwd_win_byts'},
 {'act_data_pkt_fwd': 'fwd_act_data_pkts'},
 {'min_seg_size_forward': 'fwd_seg_size_min'},
 {'Active Mean': 'active_mean'},
 {'Active Std': 'active_std'},
 {'Active Max': 'active_max'},
 {'Active Min': 'active_min'},
 {'Idle Mean': 'idle_mean'},
 {'Idle Std': 'idle_std'},
 {'Idle Max': 'idle_max'},
 {'Idle Min': 'idle_min'}]

MODEL_DIR_PATH = "C:\\Delete\\DEV\\NODEJS\\monitoring_module_v2\\monitoring_module\\python_server\\Models"
MODEL = keras.models.load_model(os.path.join(MODEL_DIR_PATH, '06_cnn.h5'))

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



@app.route('/predict', methods=['GET','POST'])
def predict():
    collection = create_connection("10")
    
    item = collection.find_one({});
    print(item)

    response = jsonify({'STATUS':'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

@app.route('/train', methods=['GET','POST'])
def train():
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
    collection = create_connection(dev_id=dev_id)
    flows =  list(collection.find({}, {"_id":False}))
    print(len(flows[0].keys()))
    response = jsonify(flows)

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