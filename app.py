import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, escape
from flask_mysqldb import MySQL
from flask import json
import simplejson

app = Flask(__name__)

app.config['MYSQL_HOST'] = '172.17.0.3'
app.config['MYSQL_USER'] = 'mysqld'
app.config['MYSQL_PASSWORD'] = 'teste1234'
app.config['MYSQL_DB'] = 'music'
mysql = MySQL(app)

@app.route('/login')
def logon():
        return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():

    firstName = request.form['fname']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM music WHERE firstname ='" + firstName + "'")
    data = cur.fetchone()
    if data is None:
       return "invalid user"
    else:
       return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        prof = details['prof']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO music(firstName, lastName, prof) VALUES (%s, %s, %s)", (firstName, lastName, prof))
        mysql.connection.commit()
        cur.close()
    return render_template('index.html')

@app.route('/show')
def show():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,firstname,lastname,prof FROM music")
    data = cur.fetchall()
    return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
