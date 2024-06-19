# app.py
import logging
import sys

import os
import unittest
import coverage

from flask.cli import FlaskGroup
from flask_migrate import Migrate, log
from project.server.server import app, db


logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(levelname)s - %(message)s')


def log_flags():
    log.log(logging.WARNING, "Command-line arguments:")
    for arg in sys.argv:
        log.log(logging.WARNING, arg)


log_flags()

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/configs.py',
        'project/server/*/server.py'
    ]
)
COV.start()

migrate = Migrate(app, db)

cli = FlaskGroup(app)


@cli.command("test")
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command("cov")
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@cli.command("create_db")
def create_db():
    """Creates the db tables."""
    db.create_all()


@cli.command("drop_db")
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    log_flags()
    try:
        cli()
    except Exception as e:
        logging.error("An error occurred while running the CLI: %s", str(e))
