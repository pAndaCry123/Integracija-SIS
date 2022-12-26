import datetime
import json

from app import app
from flask_cors import cross_origin
from flask import request
from service import ServiceBus

@app.route('/api/upload_file', methods =['POST'])
@cross_origin()
def upload_file():

    ret_value = ServiceBus().upload_file_and_store(request.files['file'])
    return {'message': True}


@app.route('/api/train_model', methods = ['POST'])
@cross_origin()
def train_model():
    values = json.loads(request.data.decode('utf-8'))
    start_date = datetime.datetime.strptime(values['start_date'] ,'%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(values['end_date'] ,'%Y-%m-%d').date()
    ret_val = ServiceBus().train_data(start_date, end_date)
    return {'message': True}


@app.route('/api/predict_model', methods = ['POST'])
@cross_origin()
def predict_model():
    values = json.loads(request.data.decode('utf-8'))
    start_date = datetime.datetime.strptime(values['select_date'],'%Y-%m-%d').date()
    days = int(values['number_days'])
    ret_val = ServiceBus().predict_data(start_date,days)
    return {'message': True}
