from flask import request, jsonify, send_file
import sqlite3
import bcrypt
import os, io
import secrets
import base64

def listfiles(db):
    username = request.form.get('username')

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT id from Users WHERE username = ?', (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('SELECT file_name, file_size FROM UserFiles WHERE user_id = ?', (user_id,))
    filelist = cursor.fetchall()
    #conn.commit()
    conn.close()

    if len(filelist) > 0:
        retlist = []
        for f, size in filelist:
            retlist.append((f.decode('utf-8'), size/1024.))
        return jsonify({'message': 'Listing succeed',
                        'filelist': retlist}), 201
    else:
        return jsonify({'message': 'Listing failed'}), 404

def createfile(db):
    filedata = request.files['file'].read()
    username = request.form.get('username')
    filename = request.form.get('filename').encode('utf-8')
    filesize = len(filedata)
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id from Users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO UserFiles (user_id, file_name, file_data, file_size)
        VALUES (?, ?, ?, ?)
    ''', (user_id, filename, filedata, filesize,))
    conn.commit()
    conn.close()

    message = f"File stored successfully (size: {filesize/1024:.2f} kB)"
    print(message)
    return jsonify({"message": message}), 201

def requestfile(db):
    #import pdb; pdb.set_trace()
    username = request.form.get('username')
    filename = request.form.get('filename').encode('utf-8')
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id from Users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''
        SELECT file_data, file_size from UserFiles WHERE (user_id, file_name) = (?, ?)
    ''', (user_id, filename,))
    #conn.commit()
    filedata, filesize = cursor.fetchone()
    conn.close()

    #filedata = base64.b64encode(filedata).decode('utf-8')
    message = f"File retrieved successfully (size: {filesize/1024:.2f} kB)"
    print(message)
    return send_file(
        io.BytesIO(filedata),
        download_name=request.form.get('filename'),
        mimetype='application/pdf'
    )
    # return jsonify({"message": message,
    #                 "file": filedata,
    #                 "size": filesize}), 201
