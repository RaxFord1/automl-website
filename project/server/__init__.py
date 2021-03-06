# project/server/__init__.py

import os

from flask import Flask, render_template, jsonify, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8462@localhost:5432/'


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/_add_numbers')
def add_numbers():
    print("ADD NUMBERS:::::::::")
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(a,b)
    return jsonify(result=a + b)


@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')
    