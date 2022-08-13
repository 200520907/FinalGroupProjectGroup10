from flask import Flask, render_template, json, template_rendered, Response, Request
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from datetime import datetime, timedelta
from threading import Timer
import requests
import pytz
import time
import os
import sys
import json
import schedule

load_dotenv()

app = Flask(__name__)

#scheduler = APScheduler()

def covidData_To_Json(item) -> dict:
    return {
        "id":str(item["_id"]),
        "data":item["data"]
    }

def covidDatas_To_Json(items) -> list:
    return [covidData_To_Json(item) for item in items]


conn = MongoClient("mongodb://admin:bdat2022@ac-hbakmc9-shard-00-00.sfhkzvm.mongodb.net:27017,ac-hbakmc9-shard-00-01.sfhkzvm.mongodb.net:27017,ac-hbakmc9-shard-00-02.sfhkzvm.mongodb.net:27017/?ssl=true&replicaSet=atlas-23ujg4-shard-0&authSource=admin&retryWrites=true&w=majority")
db = conn['Covid_Data']
collection_name = db["data"]

@app.route("/health", methods=["GET"])
def getHealth():
    data = covidDatas_To_Json(db.data.find())
    return Response(
            response= json.dumps(data),status=500,mimetype="application/json"
        )
@app.route("/loadDAta", methods=["GET"])
def data_load():
    for item in countries:
        print(item)
        querystring = {"country_text":item,"date":currentDate}
        r = requests.request("GET", url, headers=headers, params=querystring)
        if r.status_code == 200:
            data = r.json()
            collection_name.insert_many(data)

@app.route("/",methods=["GET"])
def getCovidData():
    try:
        data = covidDatas_serializer(db.data.find())
        print("from html")
        return render_template('index.html', data1 = Response(
            response= json.dumps(data),status=500,mimetype="application/json"
        )
)
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"msg":"Failed to retrive Data"}),status=500,mimetype="application/json"
        )
        

url = "https://covid-19-tracking.p.rapidapi.com/v1"
headers = {
    "X-RapidAPI-Key": "70ffb4e16emsh9f5eb9947f6a419p1a2ed3jsne4d2d72523ad",
    "X-RapidAPI-Host": "covid-19-tracking.p.rapidapi.com"
}

countries = ["USA","Spain","Italy","UK","India"]
yesterday = datetime.now() - timedelta(1)
currentDate = str(datetime.strftime(yesterday, '%Y-%m-%d'))



schedule.every().day.at("17:03").do(data_load)

def job():
    print('hello')

schedule.every(2).hours.do(data_load)

# while 1:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == "__main__":
    #scheduler.add_job(id="test",func = job, trigger = 'interval', seconds = 5)
    app.run(debug=True)
