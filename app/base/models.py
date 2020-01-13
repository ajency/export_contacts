# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey, DateTime, Boolean

from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None



class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    username = Column(String)
    password = Column(String)
    failed_count = Column(Integer)
    status = Column(String)
    running = Column(Boolean)

    def __repr__(self):
        return str(self.username)





class Batch(db.Model):
    __tablename__ = 'batch'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    # contacts = db.relationship("Contact",
    #                         secondary="association",
    #                         backref="batch_id")

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
