import json
import logging
import traceback
from typing import Dict

import pika

import project.server.config as cfg
from project import constants
from project.constants import RABBIT_MQ_START_TRAINING_CHANNEL


class RequestStartTraining:
    def __init__(self, full_csv_path: str, out_path: str, dataset_name: str, user_email: str, model_size: str,
                 dataset_path: str):
        self.full_csv_path = full_csv_path
        self.out_path = out_path
        self.dataset_name = dataset_name
        self.user_email = user_email
        self.model_size = model_size
        self.dataset_path = dataset_path

    def to_dict(self) -> Dict[str, str]:
        return {
            "full_csv_path": self.full_csv_path,
            "out_path": self.out_path,
            "dataset_name": self.dataset_name,
            "user_email": self.user_email,
            "model_size": self.model_size,
            "dataset_path": self.dataset_path,
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

    def validate(self) -> bool:
        # todo : finish
        if self.model_size == "" \
                or self.out_path == "" \
                or self.full_csv_path == "" \
                or self.dataset_name == "" \
                or self.user_email == ""\
                or self.dataset_path == "":
            logging.log(logging.ERROR, "validate failed for:" + self.__str__())
            return False

        return True

    @classmethod
    def from_str(cls, inputs: str):
        data = json.loads(inputs)
        return cls(**data)


def send_message_to_start_training_channel(req: RequestStartTraining):
    rabbit_mq_host = cfg.get_val(constants.RABBIT_MQ_HOST)
    if rabbit_mq_host is None:
        raise Exception("RABBIT_MQ_HOST is None. need to init config properly!")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_mq_host))
        channel = connection.channel()

        channel.queue_declare(queue=RABBIT_MQ_START_TRAINING_CHANNEL)

        if req.validate() is not True:
            logging.log(logging.ERROR, f"RequestStartTraining did not validate correctly: {str(req)}")
            return

        msg = str(req)

        channel.basic_publish(exchange='',
                              routing_key=RABBIT_MQ_START_TRAINING_CHANNEL,
                              body=msg)

        connection.close()
    except Exception as e:
        logging.log(logging.ERROR, e)
        traceback.print_stack()


# Example usage
if __name__ == "__main__":
    request = RequestStartTraining(
        full_csv_path="path/to/full_csv.csv",
        out_path="path/to/output",
        dataset_name="example_dataset",
        user_email="user@example.com",
        model_size="large"
    )

    json_str = str(request)
    print("Serialized:", json_str)

    parsed_request = RequestStartTraining.from_str(json_str)
    print("Parsed:", parsed_request)
    print("Parsed - full_csv_path:", parsed_request.full_csv_path)
