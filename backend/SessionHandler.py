from flask import request, jsonify
import sqlite3
#import asyncio
from datetime import datetime as dt

def newdata(db):
    station_id = request.headers.get('SID')
    token = request.headers.get('TOKEN')

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    data = request.get_json()
    #station_id = data['station_id']
    #token = data['token'].encode('utf-8')

    ## Get token from db for this station_id
    cursor.execute('SELECT token FROM stations WHERE id = ?', (station_id,))
    db_token = cursor.fetchone()[0]

    if token != db_token:
        conn.close()
        return jsonify({'message': 'Unrecognized token {} for station_id {}'.format(token, station_id)}), 401

    timestamp = data['timestamp'][0]
    temp = data['temperature'][0]
    hum = data['humidity'][0]
    ws = data['wspeed'][0]
    wd = data['wdirection'][0]
    rain = data['rain'][0]
    cursor.execute('''
    INSERT INTO data (station_id, datetime, temperature, humidity, wspeed, wdirection, rain)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (station_id, timestamp, temp, hum, ws, wd, rain,))
    cursor.execute('INSERT INTO sessions (station_id, token, data_id) VALUES (?, ?, ?)', (
        station_id,
        token,
        cursor.lastrowid,
    ))

    conn.commit()
    conn.close()
    return jsonify({'message': 'Data recorded succesfully from station_id={} with {}.'.format(
        station_id,
        dt.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))}), 200

def fetchdata(db):
    data = request.get_json()
    station_id = data['station_id']
    timestamp = dt.strptime(data['datatime'],
                            '%Y-%m-%d %H:%M:%S').timestamp() #requested by client

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT temperature, humidity, wspeed, wdirection, rain FROM data
    WHERE station_id == ? && datetime == ?
    ''', (station_id, timestamp,))
    payload = {"temperature": cursor.fetchone()[0],
               "humidity": cursor.fetchone()[1],
               "wspeed": cursor.fetchone()[2],
               "wdirection": cursor.fetchone()[3],
               "rain": cursor.fetchone()[4]}
    
    conn.close()
    message = 'returned requested data for station_id [} and time [}'.format(station_id, data['datatime'])
    return jsonify({'message': message, "data": payload}), 200

def updatedata(db):
    station_id = request.headers.get('SID')
    token = request.headers.get('TOKEN')

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # get token from db
    cursor.execute('SELECT token FROM stations WHERE id = ?', (station_id,))
    db_token = cursor.fetchone()[0]

    if token != db_token:
        conn.close()
        return jsonify({"error": "Unauthorized for update, check token"}), 401

    # get payload
    data = request.get_json()
    timestamp = data['timestamp']
    temp = data['temperature']
    hum = data['humidity']
    ws = data['wspeed']
    wd = data['wdirection']
    rain = data['rain']

    # try update the fields
    cursor.execute('''
        UPDATE data
        SET datetime = ?, temperature = ?, humidity = ?, wspeed = ?, wdirection = ?, rain = ?
        WHERE station_id = ?
    ''', (timestamp, temp, hum, ws, wd, rain, station_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Record updated successfully"}), 200
