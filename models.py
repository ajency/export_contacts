# -*- encoding: utf-8 -*-

import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return str(self.username)




class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    username = Column(String)
    password = Column(String)
    failed_count = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return str(self.username)





class Batch(db.Model):
    __tablename__ = 'batch'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)

    def __repr__(self):
        return str(self.id)




class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    #batch_id = Column(Integer)
    batch_id = Column(Integer, ForeignKey('batch.id'))
    email = Column(String)
    name = Column(String)
    designation = Column(String)
    profile = Column(String)
    status = Column(String)

    def __repr__(self):
        return str(self.email)




class BatchAccount(db.Model):
    __tablename__ = 'batch_accounts'

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer)
    account_id = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return str(self.id)