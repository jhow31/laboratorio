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
from login import login_user
import socketio
from charts_ import wallet
from multiprocessing import Process
from flask import request


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


def cad_json(perc):
        #print(timestamp)
                req_data = request.get_json()
                id_user = req_data['id_user']
                print(id_user)
                timestamp = datetime.datetime.now()
        #print(timestamp)
                produt = str(req_data['produto_name'])
                print(produt)
                cate = str(req_data['produto_cat'])
                print(cate)
                desc = str(req_data['produto_desc'])
                print(desc)
                quantidad = int(req_data['produto_quant'])
                valor = decimal.Decimal(req_data['produto_val'])
#       contact = float(request.form['produto_cont'])
                cur = mysql.connection.cursor()
        #cur.execute("SELECT id FROM peoples WHERE id = %s ;", [id_people])
        #id_data  = cur.fetchone();
                cur.execute("SELECT * FROM produtos WHERE produto = %s AND id_user = %s;", [produt, id_user])
                data = cur.fetchone()
                valor_venda = valor/100*perc+valor
                if data is None:
                        cur.execute("INSERT INTO estoque (produto, categoria, valor, quantidade, id_user) VALUES (%s, %s, %s, %s, %s)", (produt, cate, valor, quantidad,id_user))
                        cur.execute("INSERT INTO produtos (produto, descricao, categoria, valor, quantidade, id_user) VALUES (%s, %s, %s, %s, %s, %s)", (produt, desc, cate, valor_venda, quantidad,id_user))
                        mysql.connection.commit()
                        valor_percentual = ("select valor from estoque where produto = %s and id_user = %s;", [produt, id_user])
                        mysql.connection.commit()
                        cur.execute("select id_produto from produtos where produto=%s and id_user = %s;", [produt, id_user])
                        produt_id = cur.fetchone()
                        data_json={'Processo': "Entrada estoque", 'Produto' : produt,'ID de Produto' : produt_id,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': str(valor), 'ID_USER' : id_user, 'TimeStamp' : timestamp}
                        mbestoque.insert_one(data_json)
                        return "Cadastrado"
                else:
                        cur.execute("select id_produto from produtos where produto=%s;", [produt])
                        produt_id = cur.fetchone()
                        data_json={'Processo': "Entrada estoque", 'Produto' : produt,'ID de Produto' : produt_id,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': str(valor), 'ID_USER' : id_user, 'TimeStamp' : timestamp}
                        mbestoque.insert_one(data_json)
                        cur.execute("select sum( %s+quantidade ) total from produtos where produto =%s and id_user = %s;", [quantidad,produt, id_user])
                        data_calc = cur.fetchone()
                        for data in data_calc:
                                calc = (int(data))
                        cur.execute("update produtos  set quantidade = %s where produto = %s and id_user = %s;", [calc, produt, id_user])
#               cur.execute("INSERT INTO estoque (produto, categoria, valor, quantidade, date_now) VALUES (%s, %s, %s, %s, %s)", (produt, cate, valor, quantidad, timestamp))
                        cur.execute("select sum( %s+quantidade ) total from estoque where produto =%s and id_user = %s;", [quantidad,produt, id_user])
                        data_calc = cur.fetchone()
                        for data in data_calc:
                                calc = (int(data))
                        cur.execute("update estoque set quantidade = %s where produto = %s and id_user = %s;", [calc, produt, id_user])
                        mysql.connection.commit()
                        return "ID do usuario ja cadastrado com este Vendedor ou ID nao existe"

