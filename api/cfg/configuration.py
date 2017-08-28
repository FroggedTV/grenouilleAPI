from os.path import isfile
import os
import logging


class Config(object):
    """Basic configuration used by the application.

    Attributes:
        DEBUG: Flask debugging option.
        TESTING: Flask testing option.
        SQLALCHEMY_TRACK_MODIFICATIONS: Flask SQLalchmey track modifications 
        option.
        DATABASE_URI: Url to the database used in Flask.
    """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    HOST = '127.0.0.1'
    PORT = 9999
    SERVERNAME = 'http://127.0.0.1:9999'


def load_config(config):
    """Load a configuration for the Flask application from a specific file.

    Starts with `Config` object as a base.
    Loads `settings.cfg` if exists and readable.

    Args:
        config: Application config object to load the config into.
    """
    config.from_object('cfg.configuration.Config')
    if isfile(os.path.join(os.path.dirname(__file__), 'settings.cfg')):
        try:
            config.from_pyfile(os.path.join(os.path.dirname(__file__), 'settings.cfg'))
        except SyntaxError:
            logging.log(logging.ERROR, 'Impossible to interpret settings file, using default.')
