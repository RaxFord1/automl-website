# project/server/server.py

import json
import logging
import os
import shutil
import time
from datetime import datetime

import pandas as pd
import rarfile
import zipfile

from flask import Flask, render_template, jsonify, request, redirect
from flask import send_file
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from project import constants
from project.server import config
from project.server.rabbit_mq.start_training import send_message_to_start_training_channel, RequestStartTraining
from project.server.utils.dataset_info import get_description, get_folder_size, get_csv_dimensions, \
    get_few_file_names_from_each_category, find_first_csv_file, get_desc, count_files_in_dir_total, \
    count_files_in_dir_by_category
from project.server.utils.rar_or_zip import extract_and_delete_rar, extract_and_delete_zip

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = config.get_val('JSONIFY_PRETTYPRINT_REGULAR', False)
app.config[constants.DATASETS_FOLDER] = config.get_val(constants.DATASETS_FOLDER, os.path.join(os.getcwd(), "datasets"))

ALLOWED_EXTENSIONS = {'csv', 'rar', 'zip'}

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

    datasets_path = config.get_val(constants.DATASETS_FOLDER)
    if datasets_path is None:
        logging.log(logging.ERROR, "datasets_path not inited")
        return jsonify(result=[])

    logging.log(logging.ERROR, "EEE::" + datasets_path)

    if result is not False:
        email = result['data']['email']
        # print()
        path_to_dataset_folder = os.path.join(datasets_path, email)
        if os.path.exists(path_to_dataset_folder):
            datasets = os.listdir(path_to_dataset_folder)
            result = []
            for dataset in datasets:
                result.append(get_description(dataset, path_to_dataset_folder))

            result_dump = json.dumps(result)
            print("result", result_dump)
            return jsonify({"result": result})

    logging.log(logging.ERROR, "not authorized")
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
    result_path = config.get_val(constants.RESULTS_FOLDER, None)
    if result_path is None:
        logging.log(logging.ERROR, "constants.RESULTS_FOLDER not inited")
        return redirect("/results", error_message="constants.RESULTS_FOLDER not inited")

    model_path = rf"{result_path}/{email}/{dataset}/tuner-1/{model}/saved_model/"

    logging.log(logging.INFO, f"downloading model. model_path = {model_path}")
    if os.path.exists(model_path):
        files = os.listdir(model_path)
        if len(files) >= 1:
            file = files[0]
            # zipfile
            downloads_folder_path = config.get_val(constants.RESULTS_FOLDER, "/download_models")
            downloads_folder_path += "/download_models"
            if not os.path.exists(downloads_folder_path):
                os.makedirs(downloads_folder_path)

            path_to_zip = f"{downloads_folder_path}/{email}_{dataset}_{model}.zip"
            zipf = zipfile.ZipFile(path_to_zip, 'w', zipfile.ZIP_DEFLATED)
            zipdir(model_path, zipf)
            zipf.close()
            return send_file(path_to_zip, as_attachment=True)
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
    path_to_dataset_folder = os.path.join(config.get_val(constants.DATASETS_FOLDER, "datasets"), email, dataset_name)
    logging.log(logging.WARNING, "FULL_DATASET_PATH" + path_to_dataset_folder)

    if os.path.exists(path_to_dataset_folder):
        description = get_desc(path_to_dataset_folder)

        logging.log(logging.WARNING, "QWE"+description.get("dataset_type", "csv"))
        data_source = description.get('csv_file', find_first_csv_file(path_to_dataset_folder))
        date_created = description.get("upload_time", time.time())
        task_type = description.get("task_type", "Classification")
        data_type = description.get("dataset_type", "csv")

        result = {
            "name": str(dataset_name),
            "date": str(date_created),
            "task_type": str(task_type),
            "data_type": str(data_type)
        }

        result = {**description, **result}

        if data_type == "csv":
            df = pd.read_csv(f"{path_to_dataset_folder}/{data_source}")

            result["table"] = str(df.head(25).to_html())
            result["shape"] = str(df.shape)

            print("result", result)
            for i in result:
                print(type(result[i]))

        elif data_type == "image":
            category_has_files = get_few_file_names_from_each_category(path_to_dataset_folder+"/images", 5)

            category_has_n_files = count_files_in_dir_by_category(path_to_dataset_folder+"/images")

            result["table"] = str("<table><tbody></tbody></table>"),
            result["category_has_n_files"] = category_has_n_files
            result["category_has_files"] = category_has_files

        return jsonify({"result": result}), 200

    else:
        return jsonify(result=[])


@app.route('/__add_dataset', methods=['POST'])
def add_dataset():
    print("__ADDDATASETS___________________________________________________________", )
    print("REQUEST:::", request)
    print("ALL_DATA::::", request.form)

    task_type = request.form.get("radio_task_type", '')
    dataset_type = request.form.get("radio_data_type", '')
    dataset_name = request.form.get("dataset_name", '')
    email = request.form.get("dataset_email", '')

    if task_type == '':
        logging.log(logging.ERROR, "no task_type")
        return redirect("/datasets", error_message="no task_type")

    if dataset_type == '':
        logging.log(logging.ERROR, "no dataset_type")
        return redirect("/datasets", error_message="no dataset_type")

    if email == '':
        logging.log(logging.ERROR, "No email")
        return redirect("/datasets", error_message="No email")

    logging.log(logging.ERROR, "FILES:::" + str(request.files))
    if 'file_upload' not in request.files:
        logging.log(logging.ERROR, "No file")
        return redirect("/datasets", error_message="No file")

    logging.log(logging.ERROR, "FILES 123:::" + str(request.files['file_upload']))
    file = request.files['file_upload']
    if file.filename == '':
        logging.log(logging.ERROR, "No file 2")
        return redirect("/datasets", error_message="No file 2")

    logging.log(logging.ERROR, "FILES 321:::" + str(request.files['file_upload']))
    if file and allowed_file(file.filename):
        datasets_path = config.get_val(constants.DATASETS_FOLDER)
        logging.log(logging.ERROR, "FILES 321:::" + str(request.files['file_upload']))
        if datasets_path is None:
            logging.log(logging.ERROR, "datasets_path not inited")

            return redirect("/datasets", error_message=f"datasets_path not inited!")

        logging.log(logging.ERROR, "FILES 321:::" + str(request.files['file_upload']))
        path_dir = os.path.join(datasets_path, email, dataset_name)
        if not os.path.exists(path_dir):
            print("Creating:::", path_dir)
            os.makedirs(path_dir)

        input_file_path = os.path.join(path_dir, file.filename)
        logging.log(logging.INFO, "FILENAME::::" + input_file_path)
        file.save(input_file_path)

        description = {"task_type": task_type, "dataset_type": dataset_type, "dataset_name": dataset_name,
                       "email": email, "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        if file.filename.endswith('.csv'):
            description["size"] = os.path.getsize(input_file_path)
            description['n_cols'], description['n_rows'] = get_csv_dimensions(input_file_path)
            pass

        elif file.filename.endswith('.rar'):
            raise Exception("NOT IMPLEMENTED")
            extract_path = os.path.join(path_dir, 'images')

            extract_and_delete_rar(input_file_path, extract_path)

        elif file.filename.endswith('.zip'):
            extract_path = os.path.join(path_dir, 'images')

            extract_and_delete_zip(input_file_path, extract_path)

            dir_count = len(os.listdir(extract_path))
            description["n_classes"] = dir_count

            description["size"] = get_folder_size(extract_path)

            files_count = count_files_in_dir_total(extract_path)

            description["n_files"] = files_count

        else:
            logging.log(logging.ERROR, "Unknown extension: " + file.filename)

    file_path = os.path.join(path_dir, "description.json")
    with open(file_path, "w") as file:
        json.dump(description, file)

    logging.log(logging.INFO, "Success")
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

    datasets_path = config.get_val(constants.DATASETS_FOLDER)
    if datasets_path is None:
        logging.log(logging.ERROR, "datasets_path not inited")
        return jsonify({"result": f"Coundln't delete {dataset_name}"}), 401

    path_to_dataset_folder = os.path.join(datasets_path, email, dataset_name)

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

    model_size = constants.MODEL_LITTLE
    if str(model_size_choice) == "2":
        model_size = constants.MODEL_MEDIUM
    elif str(model_size_choice) == "3":
        model_size = constants.MODEL_LARGE

    print(f"Selected model_size: {model_size}")

    dataset_name = request.form['dataset_name_hidden']
    datasets_folder_path = config.get_val(constants.DATASETS_FOLDER)
    if datasets_folder_path is None:
        logging.log(logging.ERROR, "constants.DATASETS_FOLDER is not inited")
        return redirect("/results", error_message=f"constants.DATASETS_FOLDER is not inited")

    dataset_path = os.path.join(datasets_folder_path, user_email, dataset_name)
    if not os.path.exists(dataset_path):
        print(f"{dataset_path} not found. redirecting!")
        return redirect("/datasets", error_message=f"{dataset_path} not found. redirecting!")

    description = get_desc(dataset_path)

    data_type = description.get("dataset_type", None)

    full_csv_path = None
    if data_type is not None and data_type == "csv":
        logging.log(logging.WARNING, "QWE" + description.get("dataset_type", "csv"))
        data_source = description.get('csv_file', find_first_csv_file(dataset_path))

        full_csv_path = os.path.join(dataset_path, data_source)

    out_path = os.getenv(constants.RESULTS_FOLDER, "/tmp") + "/" + user_email + "/" + dataset_name
    if not os.path.exists(out_path):
        print(f"making new dir: {out_path}")
        os.makedirs(out_path)

    print("REQUEST:::", request)
    projectpath = request.form
    print("FORM :::", projectpath)

    send_message_to_start_training_channel(RequestStartTraining(full_csv_path=full_csv_path,
                                                                out_path=out_path, dataset_name=dataset_name,
                                                                user_email=user_email, model_size=model_size,
                                                                dataset_path=dataset_path))

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
    datasets_path = config.get_val(constants.RESULTS_FOLDER) + "/" + email + "/"
    datasets = os.listdir(datasets_path)
    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 0,
        'scalars': 100,
        'histograms': 1
    }
    print(f"DATASETS for {email}:: ", datasets)
    # from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
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
                        # event_acc = EventAccumulator(full_history_file_path, tf_size_guidance)
                        # event_acc.Reload()
                        result_dict[dataset_name][model]['accuracy'] = 1  # event_acc.Scalars('accuracy')[0].value
                        result_dict[dataset_name][model]['auc_pr'] = 1  # event_acc.Scalars('auc_pr')[-1].value
                        result_dict[dataset_name][model]['auc_roc'] = 1  # event_acc.Scalars('auc_roc')[-1].value
                        result_dict[dataset_name][model]['loss'] = 1  # event_acc.Scalars('loss')[-1].value
                        result_dict[dataset_name][model][
                            'num_parameters'] = 1  # event_acc.Scalars('num_parameters')[-1].value

    logging.log(logging.WARNING, result_dict)

    if len(result_dict) > 0:
        return jsonify({"result": result_dict}), 200

    else:
        return jsonify(result=[])
