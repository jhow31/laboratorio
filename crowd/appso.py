from flask import Flask
import base64
import os
import pygal
import json
from urllib2 import urlopen
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
import DeepL

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

myclient = pymongo.MongoClient('mongodb://root:root@192.168.0.26:27017/')
mydb = myclient["crowd"]
mbestoque = mydb["estoque"]
mbvenda = mydb["venda"]
myvenda = mydb.mbvenda


app.config['MYSQL_HOST'] = '192.168.0.26'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'crowd'
mysql = MySQL(app)



@app.route('/sell')
def firsts():
        timestamp = datetime.datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("select produto,quantidade from produtos;")
        produtos = cur.fetchall()
        print(produtos)
        for data in produtos:
                print(data[0],data[1])
	return render_template('venda.html', value=produtos)

@app.route('/sell', methods=['POST','GET'])
def sell():
        timestamp = datetime.datetime.now()
        cur = mysql.connection.cursor()
	cur.execute("select produto from produtos;")
	produtos = cur.fetchall()
	produt = str(request.form['sell_prod'])
	quantidad = int(request.form['sell_quant'])
#	cur = mysql.connection.cursor()
	cur.execute("select quantidade from produtos where produto = %s;", [produt])
	quantidade = cur.fetchone()
        for data in quantidade:
		calc_result = (int(data))
	if quantidad <= calc_result:
		cur.execute("select sum( quantidade-%s ) from produtos where produto =%s;", [quantidad,produt])
		calc = cur.fetchone()
		cur.execute("update produtos set quantidade = %s where produto = %s;", [calc, produt])
		mysql.connection.commit()
		cur.execute("select sum( valor*%s ) from produtos where produto =%s;", [quantidad,produt])
		valor_venda = cur.fetchone()
		for data in valor_venda:
			valor_venda = (int(data))
                cur.execute("select id_produto from produtos where produto=%s;", [produt])
                produt_id = cur.fetchone()		
		cur.execute("select categoria from produtos where produto=%s;", [produt])
		cate = cur.fetchone()
		data_json={'Processo': "Saida Venda", 'Produto' : produt,'ID de Produto' : produt_id,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': valor_venda, 'TimeStamp' : timestamp}
                mbvenda.insert_one(data_json)
		cur.execute("INSERT INTO venda (produto, categoria, valor, quantidade, date_now) VALUES (%s, %s, %s, %s, %s)", (produt_id, cate, valor_venda, quantidad, timestamp))
		mysql.connection.commit()
		return render_template('venda.html', venda = valor_venda, value = produtos)
	else:
#		quant_estoque = "Estoque Baixo, estoque esta em "quantidade
		return render_template('venda.html', venda = "Estoque a baixo", value=produtos)
     
@app.route('/cad_peoples')
def firstp():
	return render_template('cadastroPessoas.html')

@app.route('/cad_peoples', methods=['POST','GET'])
def cad_people():
	nome = request.form['name_vendors']
	sobrenome = request.form['subname_vendors']
	telefone = request.form['telephone_vendor']
	email = request.form['email_vendor']
	cpf = request.form['cpf_vendor']
	cep = request.form['zip_vendor']
	password = request.form['password_vendor']
	encoded = base64.b64encode(password)
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
#Preciso de uma tela com os IDs do Vendedores pra Empresa que quer consultar e cadastrar para ele
#Associacoes empresas acessam esta tela e ela e cadastro de Usuario tbm

@app.route('/cad_produtos')
def firstc():
	return render_template('cadastroProdutos.html')

@app.route('/cad_produtos', methods=['POST','GET'])
def cad():
	timestamp = datetime.datetime.now()
	#print(timestamp)
	produt = str(request.form['produto_name'])
	cate = str(request.form['produto_cat'])
	desc = str(request.form['produto_desc'])
	quantidad = int(request.form['produto_quant'])
	valor = str(request.form['produto_val'])
	id_people  = float(request.form['produto_id_vendor'])
#	contact = float(request.form['produto_cont'])
	cur = mysql.connection.cursor()
	#cur.execute("SELECT id FROM peoples WHERE id = %s ;", [id_people])
	#id_data  = cur.fetchone();
	cur.execute("SELECT * FROM produtos WHERE produto = %s;", [produt])
	data = cur.fetchone()
	if data is None:
		cur.execute("INSERT INTO produtos (produto, descricao, categoria, valor, quantidade) VALUES (%s, %s, %s, %s, %s)", (produt, desc, cate, valor, quantidad))         
		mysql.connection.commit()
		cur.execute("select id_produto from produtos where produto=%s;", [produt])
		produt_id = cur.fetchone()
 		data_json={'Processo': "Entrada estoque", 'Produto' : produt,'ID de Produto' : produt_id,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': valor, 'TimeStamp' : timestamp}
		mbestoque.insert_one(data_json)
		return render_template('cadastroProdutos.html', value="Cadastrado")
	else:
                cur.execute("select id_produto from produtos where produto=%s;", [produt])
		produt_id = cur.fetchone()
		data_json={'Processo': "Entrada estoque", 'Produto' : produt,'ID de Produto' : produt_id,'Categoria' : cate,'Quantidade' : quantidad, 'Valor': valor, 'TimeStamp' : timestamp}
		mbestoque.insert_one(data_json)
                cur.execute("select sum( %s+quantidade ) total from produtos where produto =%s;", [quantidad,produt])
                data_calc = cur.fetchone()
                for data in data_calc:
                        calc = (int(data))
                print(calc)
		cur.execute("update produtos  set quantidade = %s where produto = %s;", [calc, produt])
                cur.execute("INSERT INTO estoque (produto, categoria, valor, quantidade, date_now) VALUES (%s, %s, %s, %s, %s)", (produt_id, cate, valor, quantidad, timestamp))
                mysql.connection.commit()
		return render_template('cadastroProdutos.html', value="ID do usuario ja cadastrado com este Vendedor ou ID nao existe")

@app.route('/dashboard')
def firstd():
	cur = mysql.connection.cursor()
	cur.execute("SELECT produto,quantidade FROM estoque")
	data1 = cur.fetchall()
	return render_template('dashboard.html', value=data1)

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
	cur = mysql.connection.cursor()
	produt = request.form['sell_prod']
	cur.execute("SELECT produto,quantidade,valor FROM estoque")
	data1 = str(cur.fetchall())
	cur.execute("select sum( valor*quantidade ) total from estoque where produto =%s;", [produt])
	data = int(cur.fetchone())
	return render_template('dashboard.html', value=data, value2=data1)
     

@app.route('/consult')
def consult():
	return render_template("teste.html")

@app.route('/consult', methods=['GET','POST'])
def consulting():
#	firstName = request.form['fname']
#	lastName = request.form['lname']
#	prof = request.form['prof']
	cur = mysql.connection.cursor()
	cur.execute("SELECT quantidade produto FROM produto;")
	data = cur.fetchone()
	return render_template('teste.html', value=data)

@app.route("/simple_chart")
def chart():
        chart2 = pygal.Line()
        chart2(1, 2, 3, fill=True)
        chart2.add('', [3, 2, 1], dot=False)
	chart = pygal.HorizontalBar()
	cur = mysql.connection.cursor()
	cur.execute("select produto, quantidade from produtos;")
	data = cur.fetchall()
	print(data)
	for row in data:
		chart.add(row[0], [row[1]])
	return chart.render_response()

@app.route("/simple_chart2")
def chart2():
#	smtp.email_sender()
	timestamp = datetime.datetime.now()
	time2 = timestamp  - datetime.timedelta(days=30)
	print(time2)
        chart = pygal.HorizontalBar()
        cur = mysql.connection.cursor()
        cur.execute("select produto, quantidade from produtos;")
        data2 = cur.fetchall()
	documents = list(mbvenda.find())
#	print(documents.append("Produtos"))
	x = []
	for x in documents:
		if x["TimeStamp"] < time2:
		#	print(x["Produto"],x["Categoria"],x["Valor"],x["Quantidade"])
			chart.add(x["Produto"], x["Quantidade"])
        return chart.render_response()

@app.route("/simple_chart3")
def chart3():
#       smtp.email_sender()
        timestamp = datetime.datetime.now()
        time2 = timestamp  - datetime.timedelta(days=30)
        chart2 = pygal.Line()
	chart2(1, 2, 3, fill=True)
	chart2.add('', [3, 2, 1], dot=False)
	chart = pygal.HorizontalBar()
        cur = mysql.connection.cursor()
        cur.execute("select produto, quantidade from produtos;")
        data2 = cur.fetchall()
        documents = list(mbvenda.find())
        x = []
#	print(documents["Quantidade"])
        for x in documents:
                if x["TimeStamp"] < time2:
                        print(x["Produto"],x["Categoria"],x["Valor"],x["Quantidade"])
#                        chart.add(x["Produto"], x["Quantidade"])
			DeepL.deepln(a,b,c)
        return chart.render_response()



@app.route('/teste')
def teste():
	documents = mydb.mbvendas.find()
	response = []
	for document in documents:
		document['_id'] = str(document['_id'])
 		response.append(document)
	return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
