# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO,send, emit
import socket
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from dotenv import load_dotenv

from settings import USER_AGENT_LIST
import random
import json

from sequence import get_main_sequences
from exporter import Exporter
from proxy_list import get_proxies


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_interval=2000, ping_timeout=120000)

# wdriver = ""
# username = "dummyuser"
# password = "dummypass"

# train_no = "13104"
# from_station = "JIAGANJ - JJG"
# to_station = "SEALDAH - SDAH"
# journey_date = "17-10-2017"
# ticket_class = "2S"
# ticket_quota = "GN"
# ticket_type = "E_TICKET"

environment = 'dev'
is_auto = True
is_headless = True
exporter = None
proxy_list = []


@app.route('/')
def index():
    return render_template('index.html')

#from views import index

# from websockets import (
#       handle_client_connect_event,
# )

@socketio.on('client_connected')
def handle_client_connect_event(json):
    global proxy_list
    #print('received json: {0}'.format(str(json)))
    emit('action', 'Connected to uplink...')

    emit('action', 'Fetching fresh proxy list from  remote...')
    proxy_list = get_proxies()
    emit('action', 'Proxy list updated...')
    print(proxy_list)

# @socketio.on('message')
# def handle_json_button(json,test):
#     # it will forward the json to all clients.
#     send(json, json=True)


@socketio.on('alert_button')
def handle_alert_event(json,test):
    # it will forward the json to all clients.
    print('Message from client was {0}'.format(json))
    emit('alert', 'Message from backendd')

@socketio.on('get_ip')
def handle_get_ip(hostname):
    driver = getChromeDriver(True)
    driver.get(hostname)
    # print("Resolving ip for host "+hostname)
    # IPHOLDER = socket.gethostbyname(hostname)
    # emit('ip_data', IPHOLDER)
    time.sleep(5)
    driver.quit()



@app.route('/webdriver_screenshots/<string:session_id>')
def webdriver_screenshots(session_id):

    return render_template('driver_screenshots.html',session_id=session_id)



@socketio.on('initiate_process')
def handle_initiate_process(payload):
    global environment
    global is_auto
    global is_headless
    environment = payload.get('env')
    is_auto = payload.get('auto')
    is_headless = payload.get('headless')
    emit('action', 'Initializing request for '+environment+' environment')
    if not is_auto:
        sequences = get_main_sequences()
        emit('steps',json.dumps(sequences))

@socketio.on('start_exporter')
def handle_start_exporter(payload):
    global environment
    global is_auto
    global is_headless
    global socketio
    global exporter
    global proxy_list
    exporter = Exporter(environment, is_auto, is_headless, socketio, proxy_list)
    emit('action', 'Starting exporter...')
    emit('action', 'Exporter session ID: '+exporter.session_id)
    emit('action', 'Started executor...')
    sequences = get_main_sequences()
    selected_sequences = []
    if is_auto:
        emit('action', 'Preparing to auto run all the sequences...')
        selected_sequences = sequences
    else:
        emit('action', 'Preparing to run selected sequence...')
        selected_sequences = payload.get('steps')

    for sequence in selected_sequences:
        sequence_title = sequences[sequence]
        emit('action', 'Started Sequence: ' + sequence_title + ' ...')
        getattr(exporter.executor, 'step_' + sequence)()

    # emit('action', 'Closing web driver instance...')
    # exporter.close_web_driver()


@socketio.on('gmail_otp_login')
def handle_gmail_otp_login(payload):
    global exporter
    emit('action', 'OTP entered is ' + payload.get('otp') + ' ...')
    exporter.executor.gmail.gmail_handler.gmail_otp_login(payload.get('otp'))



# common input
@socketio.on('exception_user_single_response')
def handle_exception_user_single_response(payload):
    global exporter
    print("payload")
    print(payload)
    handler = str(payload.get('handler')).strip()
    user_input = str(payload.get('user_input')).strip()
    emit('action', "User's response: " + user_input + ' ...')
    # check type of handler
    if handler == 'linkedin_exception_handler':
        exporter.executor.linkedin.linkedin_handler.process_exception(user_input)
    elif handler == 'linkedin_retry_login_handler':
        exporter.executor.linkedin.process_retry_login(user_input)
    elif handler == 'linkedin_email_verification_handler':
        exporter.executor.linkedin.linkedin_handler.email_pin_verify(user_input)
    elif handler == 'gmail_exception_handler':
        exporter.executor.gmail.gmail_handler.process_exception(user_input)
    elif handler == 'gmail_retry_login_handler':
        exporter.executor.gmail.process_retry_login(user_input)
    else:
        exporter.executor.logger.error('Unable to process request')





if __name__ == '__main__':
    #load_dotenv()
    socketio.run(app,debug=True,host='0.0.0.0')

