# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os
import os.path
from os import path

from sequence import get_main_sequences
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
    image_path = 'static/driver_screenshots/'+session_id
    images = []
    if path.exists(image_path):
        images = os.listdir(image_path)
        images = [session_id+'/' + file for file in images]
    return render_template('driver_screenshots.html',images=images)



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
    sequences = get_main_sequences()


    for account in ACCOUNTS:
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
                is_success = getattr(executor, 'step_' + sequence)()

            if not is_success:
                emit('action', 'Error performing the Sequence: ' + sequence_title + ' ...')
                break

        emit('action', 'Closing web driver instance...')
        executor.driver.close()
        emit('action', '######## CLOSED WEBDRIVER FOR SESSION #: '+executor.session_id+" ##########")


@socketio.on('gmail_otp_login')
def handle_gmail_otp_login(payload):
    global executor
    emit('action', 'OTP entered is ' + payload.get('otp') + ' ...')
    executor.gmail_handler.gmail_otp_login(payload.get('otp'))



# common input
@socketio.on('exception_user_single_response')
def handle_exception_user_single_response(payload):
    global executor
    print("payload")
    print(payload)
    handler = str(payload.get('handler')).strip()
    user_input = str(payload.get('user_input')).strip()
    emit('action', "User's response: " + user_input + ' ...')
    # check type of handler
    if handler == 'linkedin_exception_handler':
        executor.linkedin.linkedin_handler.process_exception(user_input)
    elif handler == 'linkedin_retry_login_handler':
        executor.linkedin.process_retry_login(user_input)
    elif handler == 'linkedin_email_verification_handler':
        executor.linkedin.linkedin_handler.email_pin_verify(user_input)
    elif handler == 'gmail_exception_handler':
        executor.gmail.gmail_handler.process_exception(user_input)
    elif handler == 'gmail_retry_login_handler':
        executor.gmail.process_retry_login(user_input)
    else:
        executor.logger.error('Unable to process request')




if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0')

