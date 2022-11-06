from flask import Flask, request, jsonify, render_template, session, redirect, url_for, session
import requests
import pandas as pd
import numpy as np
import joblib
from datetime import date,datetime

model=joblib.load("model/xgb_model.pkl")
dv=joblib.load("model/feature_vect.pkl")

def days_calculator(date):
    travel_date = datetime.strptime(date,'%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')
    today = datetime.strptime(today,'%Y-%m-%d')
    days = (travel_date-today).days
    return str(days)

def check_data(data):
    for key in data:
        if data[key] == "":
            return False
    return True

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def getvalue():
    new_data=[{
        "source_city":request.form['source_city'],
        "destination_city":request.form['destination_city'],
        "airline":request.form['airline'],
        "departure_time":request.form['departure_time'],
        "arrival_time":request.form['arrival_time'],
        "stops":request.form['stops'],
        "date":request.form['date']
      }]
    

    if check_data(new_data[0])==False:
        return "Please add all the field"

    sc = new_data[0]['source_city']
    ds = new_data[0]['destination_city']

    if  sc==ds:
        return "Source and Destination city are the same"

    date = new_data[0]['date']
    new_data[0]['date']=int(days_calculator(date))

    if new_data[0]['date']<0:
        return "Enter valid date: You can travel in the past"

    new_data_transform = dv.transform(new_data)
    res = model.predict(new_data_transform)
    return render_template('index.html', res = res[0])

if __name__ =='__main__':
    app.run(debug=True)