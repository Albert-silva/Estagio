from flask import Flask
from modules.auth.rotas import auth_rotas
from flask_cors import CORS
from database import mysql

app = Flask(__name__)
CORS (app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rootroot'
app.config['MYSQL_DATABASE_DB'] = 'compsis'

mysql.init_app(app)

app.register_blueprint(auth_rotas)

app.run("localhost", 5000)