import logging
import os
import time

import pandas as pd
import pika
import sys
from absl import app
from absl import flags

import project.constants as proj_constants
from model_search import constants
from model_search import single_trainer
from model_search.data import csv_data, image_data
from project.server import config
from project.server.rabbit_mq.start_training import RequestStartTraining
from project.server.utils.check_before_traininig import check_image_sizes
from project.server.utils.dataset_info import get_desc


def start_training_image(dataset_path, out_path, owner_name, experiment_name, model_size, images_sizes: (int, int)):
    spec = constants.DEFAULT_CNN

    if model_size == "little":
        number_models = 5
        train_steps = 100
    elif model_size == "medium":
        number_models = 10
        train_steps = 1000
    else:
        number_models = 20
        train_steps = 10000

    trainer = single_trainer.SingleTrainer(
        # data=csv_data.Provider(label_index=0, logits_dimension=2, record_defaults=logits_defaults,
        #                        filename=data_filename),
        # spec=constants.DEFAULT_DNN)
        data=image_data.Provider(
            input_dir=dataset_path,
            image_height=images_sizes[0],
            image_width=images_sizes[1],
            eval_fraction=0.2),
        spec=constants.DEFAULT_CNN)

    # number_models = 15
    # train_steps = 100

    trainer.try_models(
        number_models=number_models,
        train_steps=train_steps,
        eval_steps=10,
        root_dir=out_path,  # "/tmp/run_example3",
        batch_size=64,
        experiment_name=experiment_name,  # "example3",
        experiment_owner=owner_name)  # "model_search_user")


def start_training_csv(data_filename, out_path, owner_name, experiment_name, model_size):
    df = pd.read_csv(data_filename)

    logits_defaults = []
    for i in df.dtypes:
        if i.base.name == "float64":
            logits_defaults.append(0.0)
        elif i.base.name == "int64":
            logits_defaults.append(0)
        else:
            raise TypeError("Unknown datatype")

    try:
        label_index = df.columns.get_loc("target")
    except KeyError:
        try:
            label_index = df.columns.get_loc("label")
        except KeyError:
            label_index = 0

    if model_size == "little":
        number_models = 5
        train_steps = 100
    elif model_size == "medium":
        number_models = 10
        train_steps = 1000
    else:
        number_models = 20
        train_steps = 10000

    trainer = single_trainer.SingleTrainer(
        data=csv_data.Provider(label_index=0, logits_dimension=2, record_defaults=logits_defaults,
                               filename=data_filename),
        spec=constants.DEFAULT_DNN)

    # number_models = 15
    # train_steps = 100

    trainer.try_models(
        number_models=number_models,
        train_steps=train_steps,
        eval_steps=10,
        root_dir=out_path,  # "/tmp/run_example3",
        batch_size=64,
        experiment_name=experiment_name,  # "example3",
        experiment_owner=owner_name)  # "model_search_user")


def start_training(request: RequestStartTraining):
    data_filename = request.full_csv_path
    out_path = request.out_path
    owner_name = request.user_email
    experiment_name = request.dataset_name
    model_size = request.model_size
    dataset_path = request.dataset_path

    sys.argv = sys.argv[:1]
    try:
        app.run(lambda argv: None)
    except:
        pass

    description = get_desc(dataset_path)
    data_type = description.get("dataset_type", None)
    if data_type is None:
        logging.log(logging.ERROR, "dataset_type is not None")
        return

    if data_type == "csv":
        start_training_csv(data_filename, out_path, owner_name, experiment_name, model_size)
    elif data_type == "image":
        # images_size = (100, 100)
        dataset_path = dataset_path + "/images"
        images_size = check_image_sizes(dataset_path)
        start_training_image(dataset_path, out_path, owner_name, experiment_name, model_size, images_size)


def callback(ch, method, properties, body):
    received = body.decode()
    logging.log(logging.ERROR, f" [x] Received {received}")

    request = RequestStartTraining.from_str(received)
    logging.log(logging.ERROR, f" [x] request: {str(request)}")

    if not request.validate():
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.log(logging.ERROR, " [x] request.validate failed")

    start_training(request)

    logging.log(logging.ERROR, " [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    rabbit_mq_host = config.get_val(proj_constants.RABBIT_MQ_HOST, None)
    if rabbit_mq_host is None:
        raise Exception("RABBIT_MQ_HOST is not defined in config")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_host))
    channel = connection.channel()

    channel.queue_declare(queue=proj_constants.RABBIT_MQ_START_TRAINING_CHANNEL)

    channel.basic_consume(queue=proj_constants.RABBIT_MQ_START_TRAINING_CHANNEL, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
