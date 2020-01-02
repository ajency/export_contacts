# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os
import os.path
from os import path

from sequence import get_main_sequences, get_selected_sequences, generate_sequence_tree
from executor import Executor
from proxy_list import get_proxies

from settings import ACCOUNTS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_interval=2000, ping_timeout=120000)

environment = 'dev'
is_auto = True
is_headless = True
executor = None
proxy_list = []
config_accounts = ACCOUNTS


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('client_connected')
def handle_client_connect_event(payload):
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
    image_path = 'static/driver_screenshots/'+session_id
    images = []
    if path.exists(image_path):
        images = os.listdir(image_path)
        images = [session_id+'/' + file for file in images]
    return render_template('driver_screenshots.html',images=images)



@app.route('/export_contacts/<string:session_id>')
def export_contacts(session_id):
    csv_path = 'static/csv/'+session_id
    files = []
    if path.exists(csv_path):
        files = os.listdir(csv_path)
        files = [session_id+'/' + file for file in files]
    return render_template('export_contacts.html',files=files)



@socketio.on('initiate_process')
def handle_initiate_process(payload):
    global environment
    global is_auto
    global is_headless
    global config_accounts
    environment = payload.get('env')
    is_auto = payload.get('auto')
    is_headless = payload.get('headless')

    if 'accounts' in payload:
        config_accounts = json.loads(payload.get('accounts'))
        print(config_accounts)

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
    global executor
    global proxy_list
    global config_accounts
    sequences = get_main_sequences()



    sequence_tree = generate_sequence_tree(is_auto, payload, config_accounts)
    emit('sequence_tree', json.dumps(sequence_tree))



    for account in config_accounts:
        executor = Executor(environment, is_auto, is_headless, socketio, proxy_list, account)
        emit('action', 'Starting executor for linkedIn account: '+account.get('linkedIn').get('username'))
        emit('action', 'executor session ID: ' + executor.session_id)
        emit('active_screenshots_link', executor.session_id)

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
                sequence_title = 'Email operation'
                is_success = getattr(executor, 'step_email_operation')(selected_email_sequences)
            else:
                email_id = account.get("linkedIn").get("username")
                key_name = str(sequence) + "_" + email_id.replace('.', '').replace('@', '')
                emit('tree_progress', key_name)
                is_success = getattr(executor, 'step_' + sequence)()
                if is_success:
                    emit('tree_success', key_name)
                else:
                    getattr(executor, 'step_linkedIn_logout')()
                    emit('tree_failed', key_name)

            if not is_success:
                emit('action', 'Error performing the Sequence: ' + sequence_title + ' ...')
                break

        emit('contacts_csv_link', executor.session_id)
        emit('action', 'Closing web driver instance...')
        executor.driver.close()
        emit('action', '######## CLOSED WEBDRIVER FOR SESSION #: '+executor.session_id+" ##########")


@socketio.on('gmail_otp_login')
def handle_gmail_otp_login(payload):
    global executor
    emit('action', 'OTP entered is ' + payload.get('otp') + ' ...')
    executor.gmail_handler.gmail_otp_login(payload.get('otp'))


@socketio.on('otp_submission')
def handle_otp_submission(payload):
    global executor
    emit('action', 'OTP entered is ' + payload.get('otp') + ' ...')
    if payload.get('handler') == 'linkedIn':
        getattr(executor.linkedInHandle, 'submit_' + payload.get('key'))(payload.get('otp'))
    elif payload.get('handler') == 'gmail':
        getattr(executor.gmailHandle, 'submit_' + payload.get('key'))(payload.get('otp'))
    elif payload.get('handler') == 'yahoo':
        getattr(executor.yahooHandle, 'submit_' + payload.get('key'))(payload.get('otp'))
    elif payload.get('handler') == 'aol':
        getattr(executor.aolHandle, 'submit_' + payload.get('key'))(payload.get('otp'))






if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0')

