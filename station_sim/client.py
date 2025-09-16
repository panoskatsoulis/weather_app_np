#!/usr/bin/env python3
import requests
#import socket ## if not on an extra interface, this is not needed
import random
import pandas as pd
#import asyncio
import time

class Station:
    def __init__(self, _id, _token, _targeturl):
        self._interval = 60 # sec
        self._id = _id
        self._token = _token
        self._header = {'SID' : _id, 'TOKEN' : _token}
        self._backend = _targeturl
        self._buffer = pd.DataFrame({
            'timestamp': [], # timestamp
            'temperature': [], # oC
            'humidity': [], # %
            'wspeed': [], # m/s
            'wdirection': [], # 16-point compass
            'rain': [] # mm
        })

    def set_interval(self, _interval):
        self._interval = _interval

    def simulate_measurement(self):
        new_datapoint = {
            'timestamp': [time.time()], # timestamp
            'temperature': [random.uniform(-10, 50)], # oC
            'humidity': [random.uniform(0, 100)], # %
            'wspeed': [random.uniform(0, 40)], # m/s
            'wdirection': [random.choice(['N', 'NNE', 'NE',
                                          'ENE', 'E', 'ESE',
                                          'SE', 'SSE', 'S',
                                          'SSW', 'SW', 'WSW',
                                          'W', 'WNW', 'NW',
                                          'NNW'])], # 16-point compass
            'rain': [random.uniform(0, 15)] # mm
        }
        self._buffer.loc[len(self._buffer)] = new_datapoint # append to the buffer

    def send_datapoint(self):
        if len(self._buffer) == 0:
            return
        # get first item
        payload = self._buffer.loc[0].to_dict()
        r = requests.post(self._backend+'/newdata', json=payload, headers=self._header)
        print(f"Status: {r.status_code}, Response: {r.text}")
        if r.status_code == 200:
            self._buffer.drop(0)
            self._buffer.reset_index(drop=True)

    def run(self):
        while True:
            print("Running...")
            self.simulate_measurement()
            self.send_datapoint()
            #asyncio.sleep(self._interval)
            time.sleep(self._interval)

import configparser
import threading
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("/weather_app_np/station_sim/sim-config.ini")
    backend = config["GENERAL"]["target"]
    interval = float(config["GENERAL"]["interval"])

    stations, threads = [], []
    for station_id, token in zip(config["INSTANCES"].values(),config["TOKENS"].values()):
        station = Station(station_id, token, backend)
        thread = threading.Thread(target=station.run)
        station.set_interval(interval)
        stations.append(station)
        threads.append(thread)
        thread.start()
