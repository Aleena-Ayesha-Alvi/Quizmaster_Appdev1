#App Routes

from flask import Flask,render_template,request,redirect,url_for,flash,session
from .models import *
from flask import current_app as app
from datetime import datetime

#many controller and routes here

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template('signup.html')