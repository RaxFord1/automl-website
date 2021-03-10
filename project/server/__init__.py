# project/server/__init__.py

import os
import json

from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = os.path.join(os.getcwd(), "/datasets")
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8462@localhost:5432/'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.auth.views import auth_blueprint, check_status

app.register_blueprint(auth_blueprint)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/_add_numbers')
def add_numbers():
    print("ADD NUMBERS:::::::::")
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(a, b)
    return jsonify(result=a + b)


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/datasets')
def dataset_page():
    return render_template('datasets.html')


@app.route('/__get_datasets')
def get_dataset():
    print("__GETDATASETS", )
    result = check_status()
    if result is not False:
        email=result['data']['email']
        print()
        path_to_dataset_folder = os.path.join("datasets", email)
        if os.path.exists(path_to_dataset_folder):
            datasets = os.listdir(path_to_dataset_folder)
            result = json.dumps(datasets)
            print("result", result)
            return jsonify({"result":datasets})
    return jsonify(result=[])


@app.route('/__select_datasets')
def select_dataset():
    print("__GETDATASETS", )
    result = check_status()
    email=result['data']['email']
    print()
    path_to_dataset_folder = os.path.join("datasets", email)
    if os.path.exists(path_to_dataset_folder):
        datasets = os.listdir(path_to_dataset_folder)
        result = json.dumps(datasets)
        print("result", result)
        return jsonify({"result":datasets})
    else:
        return jsonify(result=[])


@app.route('/__add_dataset', methods=['POST'])
def add_dataset():
    print("__ADDDATASETS___________________________________________________________", )
    print("ALL_DATA::::",request.form)
    email = request.form['dataset_email']
    if email == "":
        return redirect("/datasets")
    path_to_dataset_folder = os.path.join("datasets", email)
    print("FILES:::", request.files)
    if 'file_upload' not in request.files:
        print("No file ")
        return redirect("/datasets")

    file = request.files['file_upload']
    if file.filename == '':
        print("No file 2")
        return redirect("/datasets")
    if file and allowed_file(file.filename):
        path_dir = os.path.join(app.config['UPLOAD_FOLDER'], email, request.form['dataset_name'])
        if not os.path.exists(path_dir):
            print("Creating:::", path_dir)
            os.makedirs(path_dir)
        filename = os.path.join(path_dir, file.filename)
        print("FILENAME::::", filename)
        print(os.getcwd())
        file.save(filename)


    print("REQUEST:::", request)
    projectpath = request.form
    print("FORM :::", projectpath)
    return redirect("/datasets")

