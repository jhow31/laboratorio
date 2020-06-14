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
#from login import login_user
#from mysql import mysql

def mysql():
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

