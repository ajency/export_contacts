# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit

from config import config_dict
from app import create_app, db
from flask_socketio import SocketIO, emit

get_config_mode = environ.get('APPSEED_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode) 
Migrate(app, db)
#socketio = SocketIO(app, ping_interval=2000, ping_timeout=120000)


# @socketio.on('client_connected')
# def handle_client_connect_event(payload):
#     emit('action', 'Connected to uplink...')

#if __name__ == '__main__':
    #socketio.run(app,debug=True,host='0.0.0.0')
    #app.run(debug=True,host='0.0.0.0', port=5000)


#export FLASK_APP=run.py
#flask run --host=0.0.0.0 --port=5000
