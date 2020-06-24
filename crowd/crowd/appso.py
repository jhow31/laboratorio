# -*- coding: utf-8 -*-
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
from cad_produtos import cad_json
from flask import request


m_cred=0,5


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


#socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def login():
	return login_user()

@app.route('/sell')
def firsts():
	if 'loggedin' in session:
		id_user = session['id_user']
		cur = mysql.connection.cursor()
		cur.execute("select produto,quantidade from produtos where id_user = %s;",[id_user])
		produtos = cur.fetchall()
		print(produtos)
		for data in produtos:
			print(data[0],data[1])
		return render_template('venda.html', value=produtos)
	else:
		return redirect(url_for("login"))

@app.route('/sell', methods=['POST','GET'])
def sell():
	if 'loggedin' in session:
		id_user = session['id_user']
		timestamp = datetime.datetime.now()
		cur = mysql.connection.cursor()
		cur.execute("select produto from produtos where id_user = %s;",[id_user])
		produtos = cur.fetchall()
		produt = str(request.form['sell_prod'])
		quantidad = int(request.form['sell_quant'])
#	cur = mysql.connection.cursor()
		cur.execute("select quantidade from produtos where produto = %s and id_user = %s;", [produt, id_user])
		quantidade = cur.fetchone()
		for data in quantidade:
			calc_result = (int(data))
		if quantidad <= calc_result:
			cur.execute("select sum( quantidade-%s ) from produtos where produto =%s and id_user = %s;", [quantidad,produt, id_user])
			calc = cur.fetchone()
			cur.execute("update produtos set quantidade = quantidade-%s where produto = %s and id_user = %s;", [quantidad, produt, id_user])
			cur.execute("update estoque set quantidade = quantidade-%s where produto = %s and id_user = %s;", [quantidad, produt, id_user])
			mysql.connection.commit()
			cur.execute("select sum( valor*%s ) from produtos where produto =%s and id_user = %s;", [quantidad,produt, id_user])
			valor_venda = cur.fetchone()
			cur.execute("UPDATE user set wallet = wallet+%s where id_user = %s", (valor_venda, id_user))
			mysql.connection.commit()
			for data in valor_venda:
				valor_venda = (int(data))
				cur.execute("select produto from produtos where produto=%s and id_user = %s;", [produt, id_user])
				produt = cur.fetchone()		
				cur.execute("select categoria from produtos where produto=%s and id_user = %s;", [produt, id_user])
				cate = cur.fetchone()
				data_json={'Processo': "Saida Venda", 'Produto' : produt,'ID de Produto' : produt,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': valor_venda, 'ID_USER' : id_user, 'TimeStamp' : timestamp}
				mbvenda.insert_one(data_json)
#		i22cur.execute("update venda set quantidade = quantidade+%s, valor = valor+%s where produto = %s;",(quantidad, valor_venda, produt))
				cur.execute("INSERT INTO venda (produto, categoria, valor, quantidade, date_now, id_user) VALUES (%s, %s, %s, %s, %s, %s)", (produt, cate, valor_venda, quantidad, timestamp, id_user))
				mysql.connection.commit()
			return render_template('venda.html', venda = valor_venda, value = produtos)
		else:
#		quant_estoque = "Estoque Baixo, estoque esta em "quantidade
			return render_template('vendas.html', venda = "Estoque a baixo", value=produtos)
	else:
		return redirect(url_for("login"))

@app.route('/cad_peoples')
def firstp():
	if 'loggedin' in session:
		return render_template('cadastroPessoas.html')
	else:
			return redirect(url_for("login"))
@app.route('/cad_peoples', methods=['POST','GET'])
def cad_people():
	if 'loggedin' in session:
		nome = request.form['name_vendors']
		sobrenome = request.form['subname_vendors']
		telefone = request.form['telephone_vendor']
		email = request.form['email_vendor']
		cpf = request.form['cpf_vendor']
		cep = request.form['zip_vendor']
		password = request.form['password_vendor']
		encode_x = password.encode("utf-8")
		encoded = base64.b64encode(encode_x)
		print(encoded)
		cur = mysql.connection.cursor()
		cur.execute("SELECT cpf FROM user  WHERE cpf  = %s;", [cpf])
		data = cur.fetchone()
		print(data)
		if data is None:
			cur.execute("INSERT INTO user (nome, sobrenome, email, telefone, cpf, cep, password) VALUES (%s,%s, %s, %s, %s, %s, %s)", (nome, sobrenome, email, telefone, cpf, cep, encoded))
			cur.execute("SELECT nome FROM user  WHERE cpf  = %s;", [cpf])
# Enviar este fetchall por e-mail porra
			data1 = cur.fetchall()
#		data2 = data1[0]
			mysql.connection.commit()
			return render_template('cadastroPessoas.html', value=(str(data1[0])))
		else:
			return render_template('cadastroPessoas.html', value="Duplicated User")
	else:
			return redirect(url_for("login"))
#Preciso de uma tela com os IDs do Vendedores pra Empresa que quer consultar e cadastrar para ele
#Associacoes empresas acessam esta tela e ela e cadastro de Usuario tbm

@app.route('/cad_produtos')
def firstc():
	if 'loggedin' in session:
		return render_template('cadastroProdutos.html')
	else:
		return redirect(url_for("login"))

@app.route('/cad_produtos', methods=['POST','GET'])
def cad():
	if 'loggedin' in session:
		id_user = session['id_user']
		print(id_user)
		timestamp = datetime.datetime.now()
	#print(timestamp)
		produt = str(request.form['produto_name'])
		cate = str(request.form['produto_cat'])
		desc = str(request.form['produto_desc'])
		quantidad = int(request.form['produto_quant'])
		valor = decimal.Decimal(request.form['produto_val'])
		id_people  = float(request.form['produto_id_vendor'])
#	contact = float(request.form['produto_cont'])
		cur = mysql.connection.cursor()
		cur.execute("SELECT lucro_perc FROM user WHERE id_user = %s;", [id_user])
		perc = cur.fetchone()
		perc = perc[0]
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
			return render_template('cadastroProdutos.html', value="Cadastrado")
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
#		cur.execute("INSERT INTO estoque (produto, categoria, valor, quantidade, date_now) VALUES (%s, %s, %s, %s, %s)", (produt, cate, valor, quantidad, timestamp))
			cur.execute("select sum( %s+quantidade ) total from estoque where produto =%s and id_user = %s;", [quantidad,produt, id_user])
			data_calc = cur.fetchone()
			for data in data_calc:
				calc = (int(data))
			cur.execute("update estoque set quantidade = %s where produto = %s and id_user = %s;", [calc, produt, id_user])
			mysql.connection.commit()
			return render_template('cadastroProdutos.html', value="ID do usuario ja cadastrado com este Vendedor ou ID nao existe")
	else:
		return redirect(url_for("login"))

@app.route("/wallet")
def wallet_():
	return wallet()
#	return chart.render_response()

@app.route("/simple_chart4")
def draw():
	try:
		graph = pygal.Line()
		graph.title = '% Change Coolness of programming languages over time.'
		graph.x_labels = ['2011','2012','2013','2014','2015','2016']
		graph.add('Python',  [15, 31, 89, 200, 356, 900])
		graph.add('Java',	[15, 45, 76, 80,  91,  95])
		graph.add('C++',	 [5,  51, 54, 102, 150, 201])
		graph.add('All others combined!',  [5, 15, 21, 55, 92, 105])
		graph_data = graph.render_data_uri()
		return render_template("graphing.html", graph_data = graph_data)
	except:
		return(Exception)

#	return render_template('plot.html', url='static/images/plot.png')
#def teste_pool():
#	import time
#	with app.app_context():
#		while True: 
#			cur = mysql.connect.cursor()
#			cur.execute("select id_user from user")
#			data = cur.fetchall()
#			for row in data:
#				id_user = int(row[0])
#				cur.execute("select sum(valor) from venda where id_user = %s;", [id_user])
#				valor_total = cur.fetchone()[0]
#				cur.execute("update user set caixa = %s where id_user = %s;", [valor_total, id_user])
#				mysql.connect.commit()

@app.route('/teste_json', methods=['POST','GET'])
def teste_jax():
	return cad_json(perc)

@app.route('/teste')
def teste():
	documents = mydb.mbvendas.find()
	response = []
	for document in documents:
		document['_id'] = str(document['_id'])
		response.append(document)
	return json.dumps(response)

if __name__ == '__main__':
#	backProc = Process(target=teste_pool)
#	backProc.start()
	app.run(host='0.0.0.0', debug=True)
