from flask import Flask
from flask import Flask, make_response
import base64
import os
import pygal
import json
#from urllib2 import urlopen
import decimal
from flask import Markup
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, escape
from flask_mysqldb import MySQL 
from datetime import time
from flask import json
from flask_table import Table, Col
import simplejson
from flask import Flask, Response
import datetime
#from flask_pymongo import PyMongo
from bson.json_util import dumps
import pymongo
import smtplib
import smtp
import pandas
import sys
import os
import networkx as nx
import matplotlib
import matplotlib.pyplot
import matplotlib.pyplot as plt
import yaml
import configparser

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

myclient = pymongo.MongoClient('mongodb://root:root@127.0.0.1:27017/')
mydb = myclient["crowd"]
mbestoque = mydb["estoque"]
mbvenda = mydb["venda"]
myvenda = mydb.mbvenda


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'crowd'
mysql = MySQL(app)


def login_user():
        cur = mysql.connection.cursor()
        value = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
                email = request.form['email']
                password = request.form['password']
                encode_x = password.encode("utf-8")
                encoded = base64.b64encode(encode_x)
                cur.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, encoded,))
                account = cur.fetchone()
                print(account)
        # Fetch one record and return result
                if account:
                        # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id_user'] = account[0]
                        session['email'] = account[6]
                        # Redirect to home page
                        return redirect(url_for('wallet'))
                else:
                        # Account doesnt exist or username/password incorrect
                        value = 'Incorrect username/password!'
        # Show the login form with message (if any)
        return render_template('login.html', value=value)
