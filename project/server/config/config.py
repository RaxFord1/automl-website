import logging
import os

from dotenv import load_dotenv

from project import constants


def print_all_vals():
    logging.log(logging.WARNING, "env variables:")
    env_vars = os.environ

    for key in env_vars.keys():
        logging.log(logging.WARNING, f"{key}: {os.getenv(key)}")


def get_val(name: str, default=None):
    return os.getenv(name, default)


_init_run = False


def init():
    global _init_run
    if _init_run:
        return

    load_dotenv()

    logging.log(logging.WARNING, "config init")

    psql_user = get_val(constants.POSTGRES_USER, "")
    psql_password = get_val(constants.POSTGRES_PASSWORD, "")
    psql_db = get_val(constants.POSTGRES_DB, "")
    psql_host = get_val(constants.POSTGRES_HOST, "")
    psql_port = get_val(constants.POSTGRES_PORT, "5432")

    database_uri = f'postgresql://{psql_user}:{psql_password}@{psql_host}:{psql_port}/{psql_db}'
    os.environ[constants.SQLALCHEMY_DATABASE_URI] = database_uri

    os.environ['APP_SETTINGS'] = "project.server.configs.DevelopmentConfig"
    os.environ['SECRET_KEY'] = "Qsq7owM3Ut"
    os.environ['JSONIFY_PRETTYPRINT_REGULAR'] = "false"
    os.environ['FLASK_APP'] = "app.py"

    print_all_vals()

    _init_run = True


init()
