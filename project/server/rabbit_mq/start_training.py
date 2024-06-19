import json
import logging
from typing import Dict

import pika

from project.constants import RABBIT_MQ_START_TRAINING_CHANNEL


class RequestStartTraining:
    def __init__(self, full_csv_path: str, out_path: str, dataset_name: str, user_email: str, model_size: str):
        self.full_csv_path = full_csv_path
        self.out_path = out_path
        self.dataset_name = dataset_name
        self.user_email = user_email
        self.model_size = model_size

    def to_dict(self) -> Dict[str, str]:
        return {
            "full_csv_path": self.full_csv_path,
            "out_path": self.out_path,
            "dataset_name": self.dataset_name,
            "user_email": self.user_email,
            "model_size": self.model_size
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

    def validate(self) -> bool:
        # todo : finish
        raise "Not Implemented"


def send_message_to_start_training_channel(req: RequestStartTraining):
    # все отправления пусть будут

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue=RABBIT_MQ_START_TRAINING_CHANNEL)

    if req.validate() is not True:
        logging.log(logging.ERROR, f"RequestStartTraining did not validate correctly: {str(req)}")
        return

    msg = str(req)

    channel.basic_publish(exchange='',
                          routing_key=RABBIT_MQ_START_TRAINING_CHANNEL,
                          body=msg)


# Example usage
if __name__ == "__main__":
    request = RequestStartTraining(
        full_csv_path="path/to/full_csv.csv",
        out_path="path/to/output",
        dataset_name="example_dataset",
        user_email="user@example.com",
        model_size="large"
    )

    print(str(request))  # Print the JSON representation of the object
