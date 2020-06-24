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
import pygal

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

def wallet():
        if 'loggedin' in session:
                cur = mysql.connection.cursor()
                id_user = session['id_user']
                cur.execute("SELECT lucro_perc FROM user WHERE id_user = %s;", [id_user])
                perc = cur.fetchone()
                perc = perc[0]
                cur.execute("select sum(valor) from venda where id_user = %s;", [id_user])
                valor_total = cur.fetchall()
#          print(valor_total[0])
                cur.execute("select produto, sum(valor*quantidade) from estoque where id_user = %s group by produto;", [id_user])
                valor_estoque = json.dumps(cur.fetchall())
                cur.execute("select  sum(valor*quantidade)from estoque where id_user = %s;", [id_user])
                valor_t_estoque = cur.fetchall()
                lucro_total = valor_t_estoque[0]
                teste = lucro_total[0]/100*perc
                cur.execute("select wallet from user where id_user = %s;", [id_user])
                wallet_value = cur.fetchone()
                wallet_value = wallet_value[0]
                print(wallet_value)
                cur.execute("select produto, sum(quantidade) as teste from estoque where id_user = %s group by produto;", [id_user])
                data = cur.fetchall()
                chart = pygal.Bar()
                for row in data:
                        chart.add(row[0], [row[1]])
#               print(data)
                        graph_produtos = chart.render_data_uri()
                cur.execute("select produto, sum(quantidade) as teste from venda where id_user = %s group by produto;", [id_user])
                data3 = cur.fetchall()
                print(data3)
                chart = pygal.Bar()
                for row in data3:
                       chart.add(row[0], [row[1]])
                       graph_vendas = chart.render_data_uri()
                return render_template("graphing.html", chart = graph_produtos, chart3 = graph_vendas, valor_total = valor_total[0], valor_estoque = valor_estoque, valor_t_estoque = valor_t_estoque[0], lucro_total = teste, wallet_value=wallet_value)
        else:
                return redirect(url_for("login"))
