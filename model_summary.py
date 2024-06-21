import tensorflow as tf

from model_search import single_trainer
from model_search.data import image_data


DEFAULT_CNN = "./model_search/configs/cnn_config.pbtxt"

trainer = single_trainer.SingleTrainer(
    data=image_data.Provider(
        input_dir=r"F:\docker_backup\images\images",
        image_height=100,
        image_width=100,
        eval_fraction=0.2),
    spec=DEFAULT_CNN)

loaded = tf.saved_model.load(r'F:\docker_backup\tuner-1\7\saved_model\1718972892')

for idx, v in enumerate(loaded.variables):
    for s in trainer._spec.blocks_to_use:
        if s in v.name:
            print(v.name)
            print(v.shape)
