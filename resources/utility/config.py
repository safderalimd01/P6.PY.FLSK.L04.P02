from flask import Flask, request, jsonify
from flask_restful import Api
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import pymysql
import os

app = Flask(__name__)
api = Api(app)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('host')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('database')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('user')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('password')
app.config["PROPAGATE_EXCEPTIONS"] = True
mysql.init_app(app)