# project/server/__init__.py

import os
import json
import pandas as pd
import shutil
import time

from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import shlex
from subprocess import Popen, PIPE

app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = os.path.join(os.getcwd(), "datasets")
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
    # print("__GETDATASETS", )
    result = check_status()
    if result is not False:
        email = result['data']['email']
        # print()
        path_to_dataset_folder = os.path.join("datasets", email)
        if os.path.exists(path_to_dataset_folder):
            datasets = os.listdir(path_to_dataset_folder)
            result = json.dumps(datasets)
            # print("result", result)
            return jsonify({"result": datasets})
    return jsonify(result=[])


@app.route('/__select_dataset')
def select_dataset():
    # print("__SELECTDATASETS", )
    result = check_status()
    if result is False:
        # print("AUTH FAILED")
        return jsonify(result=[]), 401
    email = result['data']['email']

    # print("BODY:::::", request.args)
    dataset_name = request.args['dataset']
    path_to_dataset_folder = os.path.join("datasets", email, dataset_name)
    # print("FULL_DATASET_PATH", path_to_dataset_folder)

    if os.path.exists(path_to_dataset_folder):
        dataset_files = os.listdir(path_to_dataset_folder)
        data = {}
        if "__info.json" in dataset_files:
            with open(f"{path_to_dataset_folder}/__info.json") as data_source_file:
                data = json.load(data_source_file)
        data_source = data.get('csv_file', dataset_files[0])
        date_created = data.get("date", time.time())
        task_type = data.get("task", "Classification")
        df = pd.read_csv(f"{path_to_dataset_folder}/{data_source}")
        df_shape = df.shape
        table = df.head(25).to_html()
        result = {
            "name": str(dataset_name),
            "table": str(table),
            "shape": str(df_shape),
            "date": str(date_created),
            "task_type": str(task_type)

        }
        # print("result", result)
        # for i in result:
        #    print(type(result[i]))
        return jsonify({"result": result}), 200

    else:
        return jsonify(result=[])


@app.route('/__add_dataset', methods=['POST'])
def add_dataset():
    # print("__ADDDATASETS___________________________________________________________", )
    # print("ALL_DATA::::", request.form)
    email = request.form['dataset_email']
    if email == "":
        return redirect("/datasets")
    path_to_dataset_folder = os.path.join("datasets", email)
    # print("FILES:::", request.files)
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
        # print(os.getcwd())
        file.save(filename)

    # print("REQUEST:::", request)
    projectpath = request.form
    # print("FORM :::", projectpath)
    return redirect("/datasets")


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


@app.route('/__delete_dataset', methods=['POST'])
def delete_dataset():
    print("__delete_dataset", )
    print("FORM:", request.form)
    print("DATA:", request.data)
    print("ARGS:", request.args)
    result = check_status()
    if result is False:
        # print("AUTH FAILED")
        return jsonify(result=[]), 401
    email = result['data']['email']

    # print("BODY:::::", request.args)
    dataset_name = request.form['dataset']
    path_to_dataset_folder = os.path.join("datasets", email, dataset_name)
    # print("FULL_DATASET_PATH", path_to_dataset_folder)

    if os.path.exists(path_to_dataset_folder):
        try:
            pass
            remove(path_to_dataset_folder)
            return jsonify({"result": f"deleted {dataset_name}"}), 200
        except:
            return jsonify({"result": f"Coundln't delete {dataset_name}"}), 401

    else:
        return jsonify({"result": f"deleted {dataset_name}"}), 200


@app.route('/train_model', methods=['POST'])
def train_model():
    print("__TRAIN_MODEL___________________________________________________________", )
    print("ALL_DATA::::", request.form)

    user_email = request.form['dataset_email']
    model_size_choice = request.form['model_size']

    model_size = "little"
    if str(model_size_choice) == "2":
        model_size = "medium"
    elif str(model_size_choice) == "3":
        model_size = "large"

    dataset_name = request.form['dataset_name_hidden']
    dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], user_email, dataset_name)
    if not os.path.exists(dataset_path):
        return redirect("/datasets")

    dir_files = os.listdir(dataset_path)
    csv_path = dir_files[0]
    if "__info.csv" in dir_files:
        pass#read file
    else:
        csv_path = dir_files[0]

    full_csv_path = os.path.join(dataset_path, csv_path)


    out_path = "/tmp/" + user_email

    print("REQUEST:::", request)
    projectpath = request.form
    print("FORM :::", projectpath)
    # subprocess.Popen

    # command = shlex.split('python train.py C:\\Users\\Dzund\\Projects\\model_search\\model_search\\default.csv /tmp/run_example3 -e exp1 -o qwerty1 -s little')
    command = ['python', 'train.py', full_csv_path, out_path,
               '-e', dataset_name, '-o', user_email, '-s', model_size]

    print(command)
    Popen(command, stdout=PIPE, stderr=PIPE)
    # with Popen(command, stdout=PIPE) as proc:
    #    log.write(proc.stdout.read())

    return redirect("/datasets")
