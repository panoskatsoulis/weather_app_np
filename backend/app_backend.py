from flask import Flask
from flask_cors import CORS
import InitDBHandler # function init_db
import SessionHandler # functions newdata, fetchdata, updatedata

import argparse, os

parser = argparse.ArgumentParser(description='Backend helpler that handles the database of the app.')
parser.add_argument('--port', type=int, default=5000, help='specify port where frontend is connected (default: 5000).')
parser.add_argument('--init', action='store_true', help='run the backend only to initializae a new DB file.')
parser.add_argument('--debug', action='store_true', help='run the backend in debug mode.')
args = parser.parse_args()

db = '/weather_app_np/backend/backend.db'

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = '/home/kpanos/myonlilnelawyer/backend/uploads/'
#app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpeg', 'jpg', 'png', 'txt'}
#if not os.path.exists(app.config['UPLOAD_FOLDER']):
#    os.makedirs(app.config['UPLOAD_FOLDER'])
CORS(app)

@app.route('/newdata', methods=['POST'])
def newdata():
    return SessionHandler.newdata(db)

@app.route('/fetchdata', methods=['GET'])
def fetchdata():
    return SessionHandler.fetchdata(db)

@app.route('/updatedata', methods=['PUT'])
def updatedata():
    return SessionHandler.updatedata(db)

if __name__ == "__main__":
    if args.init:
        InitDBHandler.init_db(db)
        quit(0)
    app.run(debug=args.debug, port=args.port)
