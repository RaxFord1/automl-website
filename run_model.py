import logging

import numpy as np
import tensorflow as tf

# Load the saved model
# model = tf.keras.models.load_model('/results/raxford32@gmail.com/iris/tuner-1/15/saved_model/1718824981/')

# loaded_model = tf.compat.v1.saved_model.load_v2('/results/raxford32@gmail.com/iris/tuner-1/15/saved_model/1718824981/')

imported = tf.saved_model.load('/results/raxford32@gmail.com/iris/tuner-1/15/saved_model/1718824981/')

logging.log(logging.WARNING, "   [x]  DONE ")

print("\nimported.signatures:")
print(imported.signatures)

infer = imported.signatures["serving_default"]


input_signature = infer.structured_input_signature[1]
input_keys = input_signature.keys()

print("\ninput_key:")
print(input_signature.keys())

output_signature = infer.structured_outputs

print("\noutput_signature:")
print(output_signature.keys())


class CustomModel(tf.keras.Model):
    def __init__(self, infer_function, input_key, output_keys):
        super(CustomModel, self).__init__()
        self.infer_function = infer_function
        self.input_key = input_key
        self.output_keys = output_keys

    def __call__(self, inputs):
        # inputs = tf.convert_to_tensor(inputs)
        input_dict = {}
        for i in range(len(self.input_key)):
            # print(i, inputs[0][i])
            input_dict[str(i+1)] = tf.convert_to_tensor(inputs[:, i], dtype=tf.float32)
        # input_dict = {self.input_key: inputs}
        outputs = self.infer_function(**input_dict)

        return {key: outputs[key] for key in self.output_keys}


model = CustomModel(infer, input_keys, output_signature.keys())

input_data = np.random.rand(1, 30)

predictions = model(input_data)
logging.log(logging.WARNING, "RESULTS:")
logging.log(logging.WARNING, predictions)
