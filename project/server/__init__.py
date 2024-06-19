# project/server/__init__.py

import json
import logging
import os
import shutil
import time

import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect
from flask import send_file
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from project import constants
from project.server import config
from project.server.rabbit_mq.start_training import send_message_to_start_training_channel, RequestStartTraining

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = config.get_val('JSONIFY_PRETTYPRINT_REGULAR', False)
app.config['UPLOAD_FOLDER'] = config.get_val('UPLOAD_FOLDER', os.path.join(os.getcwd(), "datasets"))

ALLOWED_EXTENSIONS = {'csv'}

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.configs.DevelopmentConfig'
)

app.config.from_object(app_settings)
app.config[constants.SQLALCHEMY_DATABASE_URI] = config.get_val(constants.SQLALCHEMY_DATABASE_URI,
                                                               'postgresql://postgres:postgres@localhost:5432/')

logging.log(logging.WARNING, f"AAA: {app.config[constants.SQLALCHEMY_DATABASE_URI]}")

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# оно должно быть здесь ибо bcrypt не импортируется иначе. мне лень рефакторить
from project.server.auth import auth_blueprint, check_status, LoginAPI, RegisterAPI, LoginForm, RegisterForm


app.register_blueprint(auth_blueprint)


@app.context_processor
def inject_forms():
    return dict(login_form=LoginForm(), register_form=RegisterForm())


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/datasets')
def dataset_page():
    return render_template('datasets.html', title="Датасети")


@app.route('/about')
def about_page():
    return render_template('about.html', title="Про нас")


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")


@app.route('/functions')
def about_functions():
    return render_template('functions.html')


@app.route('/__get_datasets')
def get_dataset():
    print("__GETDATASETS", )
    result = check_status()
    if result is not False:
        email = result['data']['email']
        # print()
        path_to_dataset_folder = os.path.join("datasets", email)
        if os.path.exists(path_to_dataset_folder):
            datasets = os.listdir(path_to_dataset_folder)
            result = json.dumps(datasets)
            print("result", result)
            return jsonify({"result": datasets})
    return jsonify(result=[])


import zipfile


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


@app.route("/models/<email>/<dataset>/<model>")
def download_model(email, dataset, model):
    print("DOWNLOAD MODEL")
    model_path = rf"D:/tmp/{email}/{dataset}/tuner-1/{model}/saved_model/"
    print(model_path)
    if os.path.exists(model_path):
        files = os.listdir(model_path)
        if len(files) >= 1:
            file = files[0]
            # zipfile
            model_to_save = rf"D:\Колледж\курсовая 4 курс\flask-jwt-auth-master\project\server\model\{email}_{dataset}_{model}.zip"
            zipf = zipfile.ZipFile(model_to_save, 'w', zipfile.ZIP_DEFLATED)
            zipdir(model_path, zipf)
            zipf.close()
            return send_file(model_to_save, as_attachment=True)
        else:
            print("No Files Here")
    else:
        print("Path not exists")
    return redirect("/results")


@app.route('/__select_dataset')
def select_dataset():
    print("__SELECTDATASETS", )
    result = check_status()
    if result is False:
        print("AUTH FAILED")
        return jsonify(result=[]), 401
    email = result['data']['email']

    print("BODY:::::", request.args)
    dataset_name = request.args['dataset']
    path_to_dataset_folder = os.path.join("datasets", email, dataset_name)
    print("FULL_DATASET_PATH", path_to_dataset_folder)

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
        print("result", result)
        for i in result:
           print(type(result[i]))
        return jsonify({"result": result}), 200

    else:
        return jsonify(result=[])


@app.route('/__add_dataset', methods=['POST'])
def add_dataset():
    print("__ADDDATASETS___________________________________________________________", )
    print("ALL_DATA::::", request.form)
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
        # print(os.getcwd())
        file.save(filename)

    print("REQUEST:::", request)
    projectpath = request.form
    print("FORM :::", projectpath)
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

    print(f"Selected model_size: {model_size}")

    dataset_name = request.form['dataset_name_hidden']
    dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], user_email, dataset_name)
    if not os.path.exists(dataset_path):
        print(f"{dataset_path} not found. redirecting!")
        return redirect("/datasets")

    dir_files = os.listdir(dataset_path)
    csv_path = dir_files[0]
    if "__info.csv" in dir_files:
        pass  # read file
    else:
        csv_path = dir_files[0]

    full_csv_path = os.path.join(dataset_path, csv_path)

    out_path = "D:/tmp/" + user_email + "/" + dataset_name
    if not os.path.exists(out_path):
        print(f"making new dir: {out_path}")
        os.makedirs(out_path)

    print("REQUEST:::", request)
    projectpath = request.form
    print("FORM :::", projectpath)
    # subprocess.Popen

    # command = shlex.split('python train.py C:\\Users\\Dzund\\Projects\\model_search\\model_search\\default.csv /tmp/run_example3 -e exp1 -o qwerty1 -s little')
    # command = ['python', 'train.py', full_csv_path, out_path,
    #            '-e', dataset_name, '-o', user_email, '-s', model_size]
    #
    # print(command)
    # Popen(command, stdout=PIPE, stderr=PIPE)

    send_message_to_start_training_channel(RequestStartTraining(full_csv_path=full_csv_path,
                                                                out_path=out_path, dataset_name=dataset_name,
                                                                user_email=user_email, model_size=model_size))
    # with Popen(command, stdout=PIPE) as proc:
    #    log.write(proc.stdout.read())

    return redirect("/results")


@app.route('/results')
def results_page():
    return render_template('results.html', title="Результати Трейну")


@app.route('/__load_results')
def load_results():
    print("__load_results #################################################################", )
    result = check_status()
    if result is False:
        print("AUTH FAILED")
        return jsonify(result=[]), 401
    email = result['data']['email']

    print("BODY:::::", request.args)
    result_dict = {}
    datasets_path = "D:/tmp/" + email + "/"
    datasets = os.listdir(datasets_path)
    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 0,
        'scalars': 100,
        'histograms': 1
    }
    print(f"DATASETS for {email}:: ", datasets)
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    for dataset_name in datasets:
        dataset_path = os.path.join(datasets_path, dataset_name)
        root_dataset_folders = os.listdir(dataset_path)
        for folder in root_dataset_folders:
            if "tuner" not in folder:
                continue
            else:

                tuner_path = os.path.join(dataset_path, folder)

                models = os.listdir(tuner_path)
                if len(models) <= 1:
                    continue

                result_dict[dataset_name] = {}
                print(tuner_path)
                print(models)

                for model in models:
                    model_path = os.path.join(tuner_path, model)
                    if len(os.listdir(model_path)) == 0:
                        continue
                    result_dict[dataset_name][model] = {}

                    eval_folder = os.path.join(model_path, "eval")
                    if not os.path.exists(eval_folder):
                        continue
                    history_file = os.listdir(eval_folder)
                    if len(history_file) != 0:
                        history_file = history_file[0]
                        full_history_file_path = os.path.join(eval_folder, history_file)
                        event_acc = EventAccumulator(full_history_file_path, tf_size_guidance)
                        event_acc.Reload()
                        result_dict[dataset_name][model]['accuracy'] = event_acc.Scalars('accuracy')[0].value
                        result_dict[dataset_name][model]['auc_pr'] = event_acc.Scalars('auc_pr')[-1].value
                        result_dict[dataset_name][model]['auc_roc'] = event_acc.Scalars('auc_roc')[-1].value
                        result_dict[dataset_name][model]['loss'] = event_acc.Scalars('loss')[-1].value
                        result_dict[dataset_name][model]['num_parameters'] = event_acc.Scalars('num_parameters')[
                            -1].value

    print(result_dict)

    if len(result_dict) > 0:
        return jsonify({"result": result_dict}), 200

    else:
        return jsonify(result=[])
