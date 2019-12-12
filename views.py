# -*- coding: utf-8 -*-
from __init__ import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')
