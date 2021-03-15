import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument("data_path", help="Path to csv file")
parser.add_argument("out_path", help="Path to directory where to store experiments")
parser.add_argument("-e", "--experiment_name", help="Name of experiment", default="experiment-1")
parser.add_argument("-o", "--owner", help="Owner of experiment", default="qwerty")
parser.add_argument("-s", "--size", help="Size of model-> 'little|medium|large'", choices=["little", "medium", "large"],
                    default="little")

args = parser.parse_args()


import pandas as pd

import model_search
from model_search import constants
from model_search import single_trainer
from model_search.data import csv_data


import sys

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS


# data_filename = "model_search/data/testdata/csv_random_data.csv"
# data_filename = r"C:\\Users\\Dzund\\Projects\\model_search\\model_search\\default.csv"
# spec = constants.DEFAULT_DNN

data_filename = args.data_path
out_path = args.out_path
owner_name = args.owner
experiment_name = args.experiment_name
model_size = args.size


sys.argv = sys.argv[:1]
try:
    app.run(lambda argv: None)
except:
    pass


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
    spec = constants.DEFAULT_DNN
elif model_size == "medium":
    number_models = 10
    train_steps = 1000
    spec = constants.DEFAULT_DNN
else:
    number_models = 20
    train_steps = 10000
    spec = constants.DEFAULT_DNN


trainer = single_trainer.SingleTrainer(
    data=csv_data.Provider(label_index=0, logits_dimension=2, record_defaults=logits_defaults,
    filename=data_filename),
    spec=spec)


number_models = 1
train_steps = 1


trainer.try_models(
    number_models=number_models,
    train_steps=train_steps,
    eval_steps=1,
    root_dir=out_path,  # "/tmp/run_example3",
    batch_size=64,
    experiment_name=experiment_name,  # "example3",
    experiment_owner=owner_name)  # "model_search_user")

# python train.py C:\\Users\\Dzund\\Projects\\model_search\\model_search\\default.csv /tmp/run_example3 -e exp1 -o qwerty1 -s little
