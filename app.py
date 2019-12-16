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

from settings import ACCOUNTS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

environment = 'dev'
is_auto = True
is_headless = True
exporter = None
proxy_list = []


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('client_connected')
def handle_client_connect_event(json):
    global proxy_list
    #print('received json: {0}'.format(str(json)))
    emit('action', 'Connected to uplink...')

    emit('action', 'Fetching fresh proxy list from  remote...')
    proxy_list = get_proxies()
    emit('action', 'Proxy list updated...')
    print(proxy_list)


@socketio.on('alert_button')
def handle_alert_event(json,test):
    # it will forward the json to all clients.
    print('Message from client was {0}'.format(json))
    emit('alert', 'Message from backendd')



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
    sequences = get_main_sequences()


    for account in ACCOUNTS:
        exporter = Exporter(environment, is_auto, is_headless, socketio, proxy_list, account)
        emit('action', 'Starting exporter for linkedIn account: '+account.get('linkedIn').get('username'))
        emit('action', 'Exporter session ID: ' + exporter.session_id)
        if is_auto:
            emit('action', 'Preparing to auto run all the sequences...')
            selected_sequences = sequences
            selected_email_sequences = sequences.get('email_operation')
        else:
            emit('action', 'Preparing to run selected sequence...')
            payload_sequences = payload.get('steps')
            selected_sequences = []
            selected_email_sequences = []
            for seq in payload_sequences:
                if seq in sequences.get('email_operation'):
                    if not 'email_operation' in selected_sequences:
                        selected_sequences.append('email_operation')
                    selected_email_sequences.append(seq)
                else:
                    selected_sequences.append(seq)

        for sequence in selected_sequences:
            sequence_title = sequences[sequence]
            if isinstance(sequence_title, dict):
                emit('action', 'Started Sequence: Email operation ...')
                getattr(exporter.executor, 'step_email_operation')(selected_email_sequences)
            else:
                emit('action', 'Started Sequence: ' + sequence_title + ' ...')
                getattr(exporter.executor, 'step_' + sequence)()


        emit('action', 'Closing web driver instance...')
        exporter.close_web_driver()
        emit('action', '######## CLOSE WEBDRIVER FOR SESSION #: '+exporter.session_id+" ##########")


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

