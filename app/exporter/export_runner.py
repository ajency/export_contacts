#!/usr/bin/env python
import json
from flask_socketio import emit
from app.base.models import Batch, Account, Contact
from sqlalchemy.sql import func
from .sequence import get_main_sequences
from .executor import Executor
from .proxy_list import get_proxies

class ExportRunner():

    def __init__(self, batch_id, **kwargs):
        self.batch_id = batch_id
        self.env = kwargs.get("env", "dev")
        self.auto = kwargs.get("auto", True)
        self.headless = kwargs.get("headless", True)
        self.accounts = kwargs.get("accounts", [])
        self.populate_proxylist()
        self.executor = None


    def populate_proxylist(self):
        emit('action', 'Fetching fresh proxy list from  remote...')
        proxy_list = get_proxies()
        self.proxy_list = proxy_list
        emit('action', 'Proxy list updated...')
        print(proxy_list)


    def run(self, payload):
        sequences = get_main_sequences()
        for account in self.accounts:
            executor = Executor(self.env, self.auto, self.headless, self.proxy_list, account)
            self.executor = executor
            emit('action', 'Starting executor for linkedIn account: ' + account.get('linkedIn').get('username'))
            emit('action', 'executor session ID: ' + executor.session_id)
            emit('active_screenshots_link', executor.session_id)

            if self.auto:
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
            emit('action', '######## CLOSED WEBDRIVER FOR SESSION #: ' + executor.session_id + " ##########")
