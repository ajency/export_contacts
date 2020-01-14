#!/usr/bin/env python
import json
from flask_socketio import emit
from app.base.models import Batch, Account, Contact
from sqlalchemy.sql import func
from .sequence import generate_sequence_tree
from .export_runner import ExportRunner

class BatchRunner():

    chunk_size = 200
    email_providers = ['yahoo','aol','outlook']

    def __init__(self, batch_id, **kwargs):
        self.batch_id = batch_id
        self.env = kwargs.get("env", "dev")
        self.auto = kwargs.get("auto", True)
        self.headless = kwargs.get("headless", True)
        self.proxy_list = kwargs.get("proxy_list", [])
        self.accounts = []
        self.export_runner = None


    def run(self):
        #batch = db.session.query(Batch).filter_by(id=self.batch_id)
        batch = Batch.query.get(self.batch_id)
        if batch is None:
            emit('validation_error', "Invalid batch id: "+self.batch_id)
            return False

        contacts = Contact.query.filter_by(batch_id=self.batch_id).all()

        self.accounts.append(self.populate_accounts(len(contacts)))

        sequence_tree = generate_sequence_tree(self.auto, {}, self.accounts)
        emit('sequence_tree', json.dumps(sequence_tree))

        self.export_runner = ExportRunner(self.batch_id, env=self.env, auto=self.auto, headless=self.headless, accounts=self.accounts)
        self.export_runner.run(None)


    def populate_accounts(self, total_records):
        accounts_list = dict()
        linkedin_account = Account.query.filter_by(type="linkedin", status="ACTIVE", running=False).order_by(
            func.random()).first()
        linkedin_data = {
            "username": linkedin_account.username,
            "password": linkedin_account.password
        }
        accounts_list["linkedIn"] = linkedin_data
        accounts_size = round(total_records / self.chunk_size)
        if (accounts_size == 0):
            accounts_size = 1

        email_data = dict()
        for i in range(accounts_size):
            account_type = self.email_providers[i]
            email_account = Account.query.filter_by(type=account_type, status="ACTIVE", running=False).order_by(
                func.random()).first()
            provider_data = []
            email_cred = {
                "username": email_account.username,
                "password": email_account.password
            }
            provider_data.append(email_cred)
            email_data[account_type] = provider_data
        accounts_list["email"] = email_data
        return accounts_list

